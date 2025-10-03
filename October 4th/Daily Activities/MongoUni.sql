use university

// insert one student
db.students.insertOne({})

db.students.insertOne({
  student_id: 1,
  name:"Rahul",
  age: 21,
  city: "Mumbai",
  course: "AI",
  marks: 85
})

db.students.insertMany([
  { student_id: 2, name: "Priya", age:22, city: "Delhi", course: "ML", marks:90},
  { student_id: 3, name: "Arjun", age: 20, city: "Bengaluru", course: "Data Science", marks:78},
  { student_id: 4, name: "Neha", age: 23, city:"Hyderabad", course: "AI", marks: 88},
  { student_id: 5, name: "Vikram", age: 21, city: "Chennai", course: "ML", marks: 95}
])

db.students.find()  //find all students

db.students.findOne({name: "Rahul"}) //find one student

db.students.find({marks:{$gt: 85}})  //find students with marks>85

db.students.find({}, { name: 1, course: 1, _id: 0})
{}
{
  name: 'Rahul',
  course: 'AI'
}
{
  name: 'Priya',
  course: 'ML'
}
{
  name: 'Arjun',
  course: 'Data Science'
}
{
  name: 'Neha',
  course: 'AI'
}
{
  name: 'Vikram',
  course: 'ML'
}

//Update one students marks
db.students.updateOne(
  { name: "Neha"},
  { $set: {marks: 92, course: "Advanced AI"}}
)

// update multiple students in AI course->add grade field
db.students.updateMany(
  {course: "AI"},
  { $set: {grade: "A"}}
)

// delete one student
db.students.deleteOne({name: "Arjun"})

// delete all students with marks<80
db.students.deleteMany({marks: { $lt: 80}})