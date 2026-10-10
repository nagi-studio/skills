# Nagi Skills

[中文](./README.md) · **English**

Companion skills for the Bilibili series *Re:从零开始的AI学习*. Each skill has an episode that explains why it works the way it does. [📺 Series (Chinese)](https://space.bilibili.com/312249633/lists/8719249?type=season)

## Install

Send this to your agent:

```
Install the skills from https://github.com/nagi-studio/skills
```

> **Agent, do this:** run `npx skills@latest add nagi-studio/skills -g -y` to install into the user's global skills directory. If you are Claude Code, you can instead ask the user to run `/plugin marketplace add nagi-studio/skills` and `/plugin install nagi-skills@nagi-studio`. When done, list the installed skills and remind the user to restart the session.

To install it yourself:

```bash
npx skills@latest add nagi-studio/skills -g
```

This uses the [skills CLI](https://github.com/vercel-labs/skills). It detects which agents you have installed (Claude Code, Codex, Cursor, Antigravity, and more) and puts the skills in each one's skills directory. `-g` installs globally so every project can use them; drop it to install into the current project only. Add `-a <agent>` to target a specific agent.

<details>
<summary>Claude Code can also install it as a plugin</summary>

```bash
/plugin marketplace add nagi-studio/skills
/plugin install nagi-skills@nagi-studio
```

</details>

## Update

Installed skills don't follow this repo on their own. When a new version is out, send this to your agent:

```
Update the skills from https://github.com/nagi-studio/skills
```

> **Agent, do this:** for each installed skill from this repo, run `npx skills@latest update <skill-name> -g -y`. If the user installed it as a Claude Code plugin, run `claude plugin marketplace update nagi-studio` and `claude plugin update nagi-skills@nagi-studio`. When done, remind the user to restart the session.

To update it yourself:

```bash
npx skills@latest update grill -g
```

Replace `grill` with the skill you want to update. Without a name, it updates every global skill on your machine, not just the ones from this repo.

<details>
<summary>Installed as a Claude Code plugin</summary>

In a terminal:

```bash
claude plugin marketplace update nagi-studio
claude plugin update nagi-skills@nagi-studio
```

Then run `/reload-plugins` in any open session, or restart.

</details>

## Skills

### Pondering

- [`grill`](./skills/pondering/grill): Questions you about a plan or idea, round by round, until the important unknowns surface. Five intensity levels. Works for any domain. [📺 Video (Chinese)](https://www.bilibili.com/video/BV1irHx6dEEf)
  - Credit: inspired by Matt Pocock's [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) (MIT), rewritten as a general-purpose version for everyone: Chinese-first, five intensity levels, and it stops once the remaining unknowns no longer change the next step.
- [`architect`](./skills/pondering/architect): Once the requirements are clear, compares two or three tech stacks and recommends one. Ranked by what you can actually maintain; each option lists the keys and permissions you would have to guard yourself. Picks up from grill's decision log.

## Maintaining

```bash
./scripts/link-skills.sh
```

Symlinks every skill in this repo straight into each agent's global skills directory. Run `git pull` in the repo to update; this bypasses the update commands above. Conventions for adding a skill are in [AGENTS.md](./AGENTS.md).
