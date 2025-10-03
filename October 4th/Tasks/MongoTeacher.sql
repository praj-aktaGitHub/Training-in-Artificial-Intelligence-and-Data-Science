db.createCollection("teachers")

db.teachers.insertOne({
  t_id: 1,
  name: "Anushka",
  dept: "CS",
  city: "Jalgaon",
  age: 24
})

db.teachers.insertMany([
  {t_id: 2, name: "Shreya", dept: "AI", city: "Pune", age: 23},
  {t_id: 3, name: "Prajakta", dept: "Data", city: "Bangalore", age: 26},
  {t_id: 4, name: "Ashwini", dept: "English", city: "Hyderabad", age: 30}
])

db.teachers.find()
{
  _id: ObjectId('68dfc0167614458dfd2de8be'),
  t_id: 1,
  name: 'Anushka',
  dept: 'CS',
  city: 'Jalgaon',
  age: 24
}
{
  _id: ObjectId('68dfc0e17614458dfd2de8bf'),
  t_id: 2,
  name: 'Shreya',
  dept: 'AI',
  city: 'Pune',
  age: 23
}
{
  _id: ObjectId('68dfc0e17614458dfd2de8c0'),
  t_id: 3,
  name: 'Prajakta',
  dept: 'Data',
  city: 'Bangalore',
  age: 26
}
{
  _id: ObjectId('68dfc0e17614458dfd2de8c1'),
  t_id: 4,
  name: 'Ashwini',
  dept: 'English',
  city: 'Hyderabad',
  age: 30
}
db.teachers.findOne({name: "Shreya"})
{
  _id: ObjectId('68dfc0e17614458dfd2de8bf'),
  t_id: 2,
  name: 'Shreya',
  dept: 'AI',
  city: 'Pune',
  age: 23
}
db.teachers.updateOne(
  {name:"Prajakta"},
  {$set: {dept: "Advanced AI"}}
)

db.teachers.deleteOne({name:"Ashwini"})
