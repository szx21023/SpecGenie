operators = {
  "operations": [
    {
      "kind": "drop_table",
      "target": {
        "by": "name",
        "value": "Teachers"
      },
      "if_exists": True
    },
    {
      "kind": "update_table",
      "target": {
        "by": "name",
        "value": "Courses"
      },
      "add_columns": [],
      "update_columns": [],
      "drop_columns": [
        "teacher_id"
      ]
    },
    {
      "kind": "update_table",
      "target": {
        "by": "name",
        "value": "Schedules"
      },
      "add_columns": [],
      "update_columns": [],
      "drop_columns": [
        "teacher_id"
      ]
    }
  ]
}