"""Calcule des rapports de contraste WCAG entre deux couleurs (voir la liste « tests » en bas).  Usage :  python3 tools/maquettes/contraste.py"""
def lin(c):
    c/=255
    return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def L(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def blend(fg,bg,a):
    f=fg.lstrip('#'); b=bg.lstrip('#')
    return '#'+''.join('%02x'%round(int(f[i:i+2],16)*a+int(b[i:i+2],16)*(1-a)) for i in (0,2,4))
def cr(a,b):
    la,lb=sorted([L(a),L(b)],reverse=True); return (la+0.05)/(lb+0.05)
tests=[
 ("B tele-title blanc .7 sur mb-2", blend('#ffffff','#8f4f5a',.7), '#8f4f5a'),
 ("B tele-title blanc .9 sur mb-2", blend('#ffffff','#8f4f5a',.9), '#8f4f5a'),
 ("B texte blanc .85 sur mb-2", blend('#ffffff','#8f4f5a',.85), '#8f4f5a'),
 ("A offre main blanc .82 sur mb-2", blend('#ffffff','#8f4f5a',.82), '#8f4f5a'),
 ("D grad fin #e0a06d sur blanc", '#e0a06d', '#ffffff'),
 ("D grad milieu #c2606f sur blanc", '#c2606f', '#ffffff'),
 ("D grad propose fin #b4632a sur blanc", '#b4632a', '#ffffff'),
 ("D grad propose milieu #ad4458 sur blanc", '#ad4458', '#ffffff'),
 ("E kicker rose #f4b8c0 sur mb", '#f4b8c0', '#753F48'),
 ("E footer paper .7 sur mb", blend('#f6ead9','#753F48',.7), '#753F48'),
 ("E footer paper .85 sur mb", blend('#f6ead9','#753F48',.85), '#753F48'),
 ("E h2 .p mb sur rose", '#753F48', '#f4b8c0'),
 ("muted sur cream", '#6b5d60', '#faf5f1'),
 ("muted sur sand (onglets D)", '#6b5d60', '#f1e8e2'),
 ("mb sur blanc", '#753F48', '#ffffff'),
 ("rose sur ink", '#f2a7b1', '#170e10'),
 ("A secteurs blanc .55 sur ink", blend('#ffffff','#170e10',.55), '#170e10'),
 ("tele-title blanc .7 sur verre sombre C", blend('#ffffff','#2a2022',.7), '#2a2022'),
 ("focus: blanc vs ink", '#ffffff', '#170e10'),
]
for n,a,b in tests: print(f"{cr(a,b):5.2f}  {n}")
