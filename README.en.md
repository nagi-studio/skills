# Nagi Skills

[中文](./README.md) · **English**

## For agents

Send this to your agent:

```
Install the skills from https://github.com/nagi-studio/skills
```

> **Agent, do this:** run `npx skills@latest add nagi-studio/skills -g -y` to install into the user's global skills directory. If you are Claude Code, you can instead ask the user to run `/plugin marketplace add nagi-studio/skills` and `/plugin install nagi-skills@nagi-studio`. When done, list the installed skills and remind the user to restart the session.

## For humans

### Install

#### Claude Code

```bash
/plugin marketplace add nagi-studio/skills
/plugin install nagi-skills@nagi-studio
```

#### Codex, Cursor, Antigravity, and other agents

```bash
npx skills@latest add nagi-studio/skills -g
```

This uses the [skills CLI](https://github.com/vercel-labs/skills). It detects which agents you have installed and puts the skills in each one's skills directory (usually `.agents/skills/`). `-g` installs globally so every project can use them; drop it to install into the current project only. Add `-a <agent>` to target a specific agent.

#### Local development

```bash
./scripts/link-skills.sh
```

Symlinks every skill in this repo into each agent's global skills directory. Run `git pull` to update.

### Skills

#### Pondering

- [`grill`](./skills/pondering/grill): Questions you about a plan or idea, round by round, until the important unknowns surface. Five intensity levels. Works for any domain. [📺 Video (Chinese)](https://www.bilibili.com/video/BV1irHx6dEEf)

### Credits

- `grill`: inspired by Matt Pocock's [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) (MIT), rewritten as a general-purpose version for everyone: Chinese-first, five intensity levels, and it stops once the remaining unknowns no longer change the next step.
