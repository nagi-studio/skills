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

### Rookie

- [`architect`](./skills/rookie/architect): Once the requirements are clear, compares two or three tech stacks and recommends one. Ranked by what you can actually maintain; each option lists the keys and permissions you would have to guard yourself. Picks up from grill's decision log. [📺 Video (Chinese)](https://www.bilibili.com/video/BV1TtpL6SEvg)
- [`prove-it`](./skills/rookie/prove-it): Makes the agent hand in evidence instead of "done": run the tests, click through the change in a real browser and screenshot it; when you correct the same mistake twice, turn it into a check that fails the next time; clean up three kinds of junk tests.
  - Credit: the idea of turning mistakes into checks that fail comes from Poteto's [correct](https://github.com/cursor/plugins/tree/main/pstack/skills/correct); the three kinds of junk tests draw on Matt Pocock's [tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd); clicking through in a real browser and screenshotting comes from [Voyager](https://github.com/voyager-crew/voyager)'s project-specific [verify-in-browser](https://github.com/voyager-crew/voyager/blob/main/.agents/skills/verify-in-browser/SKILL.md), generalised for any web project.
- [`de-slop`](./skills/rookie/de-slop): Strips the AI-slop look from a finished UI. The agent screenshots the page at desktop and mobile widths, then checks it against a list: redundant labels and helper text, gradients and glow, emoji in body text (swapped for a real icon library), nested cards, too many font sizes. It fixes what it finds and screenshots again until every item passes. Anything you correct goes into `DESIGN.md` so you never say it twice.
  - Credit: library picks and animation defer to Emil Kowalski's [pick-ui-library](https://github.com/emilkowalski/skills/tree/main/skills/pick-ui-library) and [animate](https://github.com/emilkowalski/skills/tree/main/skills/animate); the slop checklist draws on [@dingyi](https://x.com/dingyi/status/2115790005423734818)'s list of AI-slop frontend tells; the logo flow draws on [logo-design-skill](https://github.com/kaankiziltug/logo-design-skill) and [@Kubai087](https://x.com/Kubai087/status/2115674219602452656) on why AI icons look cheap.

## Maintaining

```bash
./scripts/link-skills.sh
```

Symlinks every skill in this repo straight into each agent's global skills directory. Run `git pull` in the repo to update; this bypasses the update commands above. Conventions for adding a skill are in [AGENTS.md](./AGENTS.md).
