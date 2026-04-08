# Stage 2 DOT Contract

Stage 2 is allowed only after explicit confirmation from user (for example: `确认`, `按这个来`, `继续画图`, `JSON没问题`, `已修改如下`).

During Stage 2, output must be exactly one fenced `dot` code block and nothing else.

## Mandatory DOT Styling Rules

- `rankdir=LR`
- Increase spacing to reduce overlap (set larger `nodesep` and `ranksep`)
- Node shapes:
  - Entity: `shape=box`
  - Attribute: `shape=ellipse`
  - Relationship: `shape=diamond`
- Edge styles:
  - Entity to relationship: solid
  - Attribute to entity/relationship: dashed
- Node IDs must be ASCII-only:
  - Entities: `E_xxx`
  - Attributes: `A_xxx`
  - Relationships: `R_xxx`
- Labels can be Chinese.
- Prefix PK attribute labels with `PK:` (optional `UQ:` prefix when needed).

## Rendering Mapping Guidance

- Create one entity node per `entities[].name`.
- Create one relationship node per `relationships[]`.
- Connect `from` and `to` entities to relationship node using solid edges.
- If `via_entity` is present, include junction entity and connect accordingly.
- Create attribute nodes for:
  - Entity attributes (`entities[].attributes[]`)
  - Relationship attributes (`relationships[].relationship_attributes[]`)
- Connect attributes to owner node with dashed edges.
