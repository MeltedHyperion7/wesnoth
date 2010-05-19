def write_animation(out, aa, name):
    c = [0, 0]
    for a in aa:
        count_animations(out, name, a, c)
    if c[1] > 1:
        out.write("%d (%d)" % (c[0], c[1]))
    else:
        out.write("%d" % c[0])

def count_animations(out, name, a, c):
    frames = a.get_subs("frame")
    if frames:
        c[0] += len(frames)
        c[1] += 1
    for a2 in a.get_subs("animation"):
        count_animations(out, name, a2, c)
    for a2 in a.get_subs("if"):
        count_animations(out, name, a2, c)
    for a2 in a.get_subs("else"):
        count_animations(out, name, a2, c)

def write_table_row(out, unit, color, name = None):
    # See the list at the beginning of src/unit_animation.cpp
    anim_types = [
        "attack_anim",
        "defend",
        "death",
        "idle_anim",
        "movement_anim",
        "leading_anim",
        "teleport_anim",
        "standing_anim",
        "healing_anim",
        "victory_anim",
        "poison_anim",
        "healed_anim",
        "recruit_anim",
        "levelin_anim",
        "levelout_anim",
        "extra_anim",
        "animation",
        "resistance_anim",
        "recruiting_anim",
        "pre_movement_anim",
        "post_movement_anim",
        "draw_weapon_anim",
        "sheath_weapon_anim"
    ]
    
    
    needed = {}
    for at in anim_types: needed[at] = True

    needed["healing_anim"] = False
    needed["leading_anim"] = False
    needed["teleport"] = False
    for abil in unit.get_subs("abilities"):
        if abil.get_subs("heals"):
            needed["healing_anim"] = True
        if abil.get_subs("leadership"):
            needed["leading_anim"] = True
        if abil.get_subs("teleport"):
            needed["teleport"] = True     

    if name == None: name = unit.id

    out.write("<tr><td class=\"%s\">%s</td>" % (color and "c1" or "c2", name))

    for t in anim_types:
        if needed[t]:
            aa = unit.get_subs(t)
            if t == "extra_anim":
                out.write("<td class=\"none\">")
            else:
                out.write("<td class=\"%s\">" % (aa and "ok" or "not"))
            write_animation(out, aa, t)
            out.write("</td>")
        else:
            out.write("<td class=\"none\">-</td>")

    out.write("</tr>\n")

    female = unit.get_first("female")
    if female: write_table_row(out, female, color, name + "[f]")

    for variation in unit.get_all("variation"):
        write_table_row(out, variation, color, name + "[%s]" %
            variation.get_text_val("variation_name"))

def put_units(f, us):
    f.write("<table>\n")
    f.write("<tr>\n")
    f.write("""
<th>id</th>
<th>attack</th>
<th>defend</th>
<th>death</th>
<th>idle</th>
<th>movement</th>
<th>leading</th>
<th>teleport</th>
<th>standing</th>
<th>healing</th>
<th>victory</th>
<th>poison</th>
<th>healed</th>
<th>recruit</th>
<th>level in</th>
<th>level out</th>
<th>extra</th>
<th>animation</th>
<th>resistance_anim</th>
<th>recruiting_anim</th>
<th>pre_movement_anim</th>
<th>post_movement_anim</th>
<th>draw_weapon_anim</th>
<th>sheath_weapon_anim</th>
""".lstrip())

    f.write("</tr>\n")
    
    def by_race(u1, u2):
        r1 = u1.rid
        r2 = u2.rid
        r = cmp(r1, r2)
        if r == 0: r = cmp(u1.id, u2.id)
        return r
    us.sort(by_race)
    race = None
    color = 0
    for u in us:
        if u.race != race:
            race = u.race
            color ^= 1
        write_table_row(f, u, color)

    f.write("</table>\n")

def write_table(f, wesnoth):
    f.write("""
<html>
<head>
<style type="text/css">
th {font-size: small; }
td {white-space: nowrap; width: 1px; }
td.c1 {background-color: #fff080;}
td.c2 {background-color: #80f0ff;}
td.ok {border: solid 1px; background-color: #80ff80;}
td.not {border: solid 1px; background-color: #ff8080;}
td.none {border: solid 1px; background-color: #ffffff;}
</style>
</head>
<body>
""".lstrip())
    f.write("<h1>animation statistics</h1>\n")
    f.write("<i>total frames (number of animations)</i>\n")
    
    f.write("<h2>Mainline</h2>\n")
    us = [x for x in wesnoth.unit_lookup.values() if x.campaign == "mainline"]
    put_units(f, us)
    
    f.write("<h2>Campaigns and Addons</h2>\n")
    us = [x for x in wesnoth.unit_lookup.values() if x.campaign != "mainline"]
    put_units(f, us)

    f.write("</body></html>")
    f.close()    

