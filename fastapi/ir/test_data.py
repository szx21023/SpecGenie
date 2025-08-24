ir_test_data = {
  "entities": [
    {
      "id": 1,
      "name": "Teacher",
      "description": "Represents a teacher in the university.",
      "columns": [
        {
          "name": "teacher_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "name",
          "type": "string",
          "nullable": False
        },
        {
          "name": "department",
          "type": "string",
          "nullable": True
        }
      ]
    },
    {
      "id": 2,
      "name": "Course",
      "description": "Represents a course that can be offered by a teacher",
      "columns": [
        {
          "name": "course_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "course_name",
          "type": "string",
          "nullable": False
        },
        {
          "name": "description",
          "type": "string",
          "nullable": True
        },
        {
          "name": "department",
          "type": "string",
          "nullable": True
        },
        {
          "name": "credits",
          "type": "int",
          "nullable": True
        }
      ]
    },
    {
      "id": 3,
      "name": "Student",
      "description": "Represents a student who can register for courses.",
      "columns": [
        {
          "name": "student_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "name",
          "type": "string",
          "nullable": False
        },
        {
          "name": "enrollment_year",
          "type": "int",
          "nullable": True
        },
        {
          "name": "major",
          "type": "string",
          "nullable": True
        }
      ]
    },
    {
      "id": 4,
      "name": "TeacherCourse",
      "description": "Represents the relationship between teachers and the courses they offer.",
      "columns": [
        {
          "name": "teacher_course_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "teacher_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "course_id",
          "type": "int",
          "nullable": False
        }
      ]
    },
    {
      "id": 5,
      "name": "StudentCourse",
      "description": "Represents the relationship between students and the courses they register in.",
      "columns": [
        {
          "name": "student_course_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "student_id",
          "type": "int",
          "nullable": False
        },
        {
          "name": "course_id",
          "type": "int",
          "nullable": False
        }
      ]
    }
  ],
  "apis": [
    {
      "id": 1,
      "method": "POST",
      "path": "/teacher/add",
      "request_fields": [
        "name",
        "department"
      ],
      "response_fields": [
        "teacher_id"
      ]
    },
    {
      "id": 2,
      "method": "POST",
      "path": "/student/add",
      "request_fields": [
        "name",
        "enrollment_year",
        "major"
      ],
      "response_fields": [
        "student_id"
      ]
    },
    {
      "id": 3,
      "method": "POST",
      "path": "/course/add",
      "request_fields": [
        "course_name",
        "description",
        "department",
        "credits"
      ],
      "response_fields": [
        "course_id"
      ]
    },
    {
      "id": 4,
      "method": "POST",
      "path": "/course/offer",
      "request_fields": [
        "teacher_id",
        "course_id"
      ],
      "response_fields": [
        "teacher_course_id"
      ]
    },
    {
      "id": 5,
      "method": "GET",
      "path": "/courses/available",
      "request_fields": [
        "student_id"
      ],
      "response_fields": [
        "course_id",
        "course_name",
        "description",
        "credits"
      ]
    },
    {
      "id": 6,
      "method": "POST",
      "path": "/course/register",
      "request_fields": [
        "student_id",
        "course_id"
      ],
      "response_fields": [
        "student_course_id"
      ]
    },
    {
      "id": 7,
      "method": "GET",
      "path": "/courses/student",
      "request_fields": [
        "student_id"
      ],
      "response_fields": [
        "course_id",
        "course_name",
        "credits"
      ]
    },
    {
      "id": 8,
      "method": "GET",
      "path": "/courses/teacher",
      "request_fields": [
        "teacher_id"
      ],
      "response_fields": [
        "course_id",
        "course_name",
        "description"
      ]
    }
  ]
}