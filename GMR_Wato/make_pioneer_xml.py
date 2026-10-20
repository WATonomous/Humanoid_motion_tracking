"""Regenerate GMR_Wato/humanoid_urdf/pioneer_humanoid.xml from pioneer_humanoid_mujoco.urdf.

Same recipe as the committed xml: free joint "floating_base" on base_link, collision boxes in group 3,
knee axes flipped so negative = flexed, a floor and a light. Run it inside humanoid_urdf/:

    python make_pioneer_xml.py pioneer_humanoid_mujoco.urdf pioneer_humanoid.xml
"""
import sys, mujoco
src, dst = sys.argv[1], sys.argv[2]
spec = mujoco.MjSpec.from_file(src)
spec.body("base_link").add_freejoint(name="floating_base")
for g in spec.geoms:
    if g.type == mujoco.mjtGeom.mjGEOM_BOX:
        g.group = 3
for j in ("Knee_L", "Knee_R"):          # negative = flexed, see the header comment
    spec.joint(j).axis = [-a for a in spec.joint(j).axis]
w = spec.worldbody
w.add_geom(name="floor", type=mujoco.mjtGeom.mjGEOM_PLANE, size=[0, 0, 0.05], rgba=[0.8, 0.8, 0.8, 1])
w.add_light(pos=[0, 0, 3], dir=[0, 0, -1], type=mujoco.mjtLightType.mjLIGHT_DIRECTIONAL)
spec.compile()
open(dst, "w").write(spec.to_xml())
