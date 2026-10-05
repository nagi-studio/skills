# Nagi Skills

Agent skills, following the [Agent Skills](https://code.claude.com/docs/en/skills) format (`SKILL.md` + `agents/openai.yaml`).

## Skills

### Thinking

- [`grill`](./skills/thinking/grill)：分轮追问你的计划或想法，直到重要未知暴露出来。5 档强度，任何领域都能用。

## Credits

- `grill`：思路受 Matt Pocock 的 [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)（MIT）启发，重写为面向所有人的通用版：中文、5 档追问强度、问到「剩下的未知不再影响下一步」就停。
