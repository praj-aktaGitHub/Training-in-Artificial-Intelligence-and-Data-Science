# escalation_live_agent.py
"""
LangGraph-aware Escalation Live Agent

- Consumes LangGraph AgentState (dict-like) and uses:
    - state["history"]      : user-visible chat-style history (list of {"role","text"})
    - state["messages"]     : LangChain message objects (HumanMessage, SystemMessage...)
    - state["convo_id"], state["ticket"], state["intent"]
- Creates an in-memory live session (replaceable with Redis/DB)
- Exposes methods for user/human send, join, get messages, close
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

# Import HumanMessage to identify last user message
from langchain_core.messages import HumanMessage

# -----------------------
# In-memory session store
# -----------------------
class LiveChatStore:
    sessions: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def create_session(
        cls,
        user_id: Optional[str],
        convo_id: Optional[str],
        latest_user_query: str,
        history: List[Dict[str, str]],
        ticket: Optional[Dict[str, Any]] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        sid = f"LS-{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow().isoformat()
        cls.sessions[sid] = {
            "session_id": sid,
            "created_at": now,
            "user_id": user_id,
            "convo_id": convo_id,
            "latest_user_query": latest_user_query,
            "history": history,        # chat-style history taken from state["history"]
            "ticket": ticket,
            "meta": meta or {},
            "messages": [
                {
                    "role": "system",
                    "text": (
                        "You joined a live escalation session.\n"
                        f"Latest user query: {latest_user_query}"
                    ),
                    "ts": now,
                }
            ],
            "human_joined": False,
            "closed": False,
        }
        return cls.sessions[sid]

    @classmethod
    def get_session(cls, session_id: str) -> Optional[Dict[str, Any]]:
        return cls.sessions.get(session_id)

    @classmethod
    def add_message(cls, session_id: str, role: str, text: str) -> List[Dict[str, Any]]:
        sess = cls.get_session(session_id)
        if sess is None:
            raise ValueError("session not found")
        msg = {"role": role, "text": text, "ts": datetime.utcnow().isoformat()}
        sess["messages"].append(msg)
        return sess["messages"]

    @classmethod
    def mark_human_joined(cls, session_id: str, human_id: str) -> Dict[str, Any]:
        sess = cls.get_session(session_id)
        if sess is None:
            raise ValueError("session not found")
        sess["human_joined"] = True
        sess["human_id"] = human_id
        cls.add_message(session_id, "system", f"Human support ({human_id}) joined the chat.")
        return sess

    @classmethod
    def close_session(cls, session_id: str) -> Dict[str, Any]:
        sess = cls.get_session(session_id)
        if sess is None:
            raise ValueError("session not found")
        sess["closed"] = True
        cls.add_message(session_id, "system", "Session closed by system.")
        return sess

# -----------------------
# EscalationLiveAgent
# -----------------------
class EscalationLiveAgent:
    """
    Public methods:
      - escalate_from_state(state, user_id=None) -> session dict
      - user_send(session_id, text)
      - human_send(session_id, text)
      - join_human(session_id, human_id)
      - get_messages(session_id)
      - close(session_id)
    """

    def _last_user_text_from_messages(self, messages: List[Any]) -> Optional[str]:
        # messages are LangChain message objects
        for m in reversed(messages):
            # robust: check type or attribute
            try:
                if isinstance(m, HumanMessage):
                    return getattr(m, "content", None)
            except Exception:
                # fallback if the object isn't the exact class
                content = getattr(m, "content", None)
                role = getattr(m, "role", None) or getattr(m, "type", None)
                # some message objects may have 'role' == 'user'
                if content and (role == "user" or role == "human"):
                    return content
        return None

    def escalate_from_state(self, state: Dict[str, Any], user_id: Optional[str] = None, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Create and return a live session using the LangGraph state.

        Expects `state` to be an AgentState-like dict with keys:
          - "messages": list of LangChain message objects
          - "history": list[{"role","text"}]  (chat-style)
          - "convo_id", "ticket" (optional)
        """

        # 1) Grab last human message content from state["messages"]
        last_user_text = self._last_user_text_from_messages(state.get("messages", [])) or ""

        # 2) Grab the chat-style history from state (clean entries)
        history = state.get("history", [])[:]  # shallow copy

        # 3) Include some meta so human sees where escalation came from
        meta = {
            "escalation_reason": reason or "supervisor_triggered" if state.get("escalate") else "manual",
            "intent": state.get("intent"),
            "latest_agent_output": state.get("latest_agent_output"),
        }

        # 4) Create session in LiveChatStore
        session = LiveChatStore.create_session(
            user_id=user_id,
            convo_id=state.get("convo_id"),
            latest_user_query=last_user_text,
            history=history,
            ticket=state.get("ticket"),
            meta=meta,
        )

        # 5) Optionally append a short summary message with context (first lines)
        # Prepare a short preview of the history for the human
        preview_lines = []
        for turn in history[-6:]:
            r = turn.get("role", "?").upper()
            t = (turn.get("text") or "").strip().replace("\n", " ")[:300]
            preview_lines.append(f"{r}: {t}")
        preview_text = "\n".join(preview_lines)
        if preview_text:
            LiveChatStore.add_message(session["session_id"], "system", "Recent history preview:\n" + preview_text)

        return session

    # Live chat operations ------------------------------------------------
    def user_send(self, session_id: str, text: str) -> List[Dict[str, Any]]:
        return LiveChatStore.add_message(session_id, "user", text)

    def human_send(self, session_id: str, text: str) -> List[Dict[str, Any]]:
        return LiveChatStore.add_message(session_id, "human", text)

    def join_human(self, session_id: str, human_id: str) -> Dict[str, Any]:
        return LiveChatStore.mark_human_joined(session_id, human_id)

    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        sess = LiveChatStore.get_session(session_id)
        if sess is None:
            raise ValueError("session not found")
        return sess["messages"]

    def close(self, session_id: str) -> Dict[str, Any]:
        return LiveChatStore.close_session(session_id)
