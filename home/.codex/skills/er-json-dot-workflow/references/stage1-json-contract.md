# Stage 1 JSON Contract

During Stage 1, output must be a JSON object only (no explanation, no markdown fence).

## Required Output Schema (strict)

```json
{
  "entities": [
    {
      "name": "Student",
      "source_name": "student",
      "attributes": [
        {"name": "id", "source_name": "id", "type": "int", "pk": true, "unique": true, "nullable": false},
        {"name": "gender", "source_name": "gender", "type": "varchar", "pk": false, "unique": false, "nullable": true}
      ]
    }
  ],
  "relationships": [
    {
      "name": "Enroll",
      "type": "many_to_many",
      "from": "Student",
      "to": "Course",
      "via_entity": "StudentCourse",
      "cardinality": null,
      "relationship_attributes": [
        {"name": "score", "source_name": "score", "type": "decimal"}
      ]
    }
  ],
  "assumptions": [
    "..."
  ],
  "questions": [
    "..."
  ]
}
```

## Extraction Rules

- SQL source:
  - Use `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `REFERENCES`, `UNIQUE` as authoritative.
- ORM/code source:
  - Use model/class declarations, field metadata, annotations, and explicit relation declarations.
- Thesis/requirements source:
  - Nouns imply entities.
  - “包含/字段/属性/编号” descriptions imply attributes.
  - Verb phrases imply relationships.
- Many-to-many:
  - If a junction table mainly consists of two foreign keys, infer `many_to_many`.
  - If junction table has extra business columns, place them into `relationship_attributes`.
- Unknown cardinality:
  - Set `cardinality` to `null` and add a question for user confirmation.
