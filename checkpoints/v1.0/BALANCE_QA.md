# Balance QA — V1.0

Full-clip balance analysis samples the selected authored animation.

Per sample:

1. evaluate the authored animation pose
2. compute world-space Center of Mass
3. determine supporting feet near the current ground level
4. build the support rectangle
5. test projected COM against support + balance margin

Current issue severity:

- **Warning**: COM outside support by up to 0.18 m
- **Hard**: COM outside support by more than 0.18 m

Timed issues can jump the Animation Timeline to the offending point.

This is an animation-quality diagnostic. It does not replace gameplay physics or a character controller.
