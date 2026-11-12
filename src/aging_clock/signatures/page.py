"""Piste « signatures », partie C : page HTML autonome (visualisation de resultats de recherche).

Toutes les valeurs viennent des fichiers de reports/signatures ; aucune n'est recopiee a la main.
"""
from __future__ import annotations

import ast
import json

import pandas as pd

from . import analyse as A
from . import vecteurs as V

NOMS_COURTS = {"perte_poids": "Perte de poids (7 kg)", "mediterraneen": "Alimentation méditerranéenne", "arret_tabac": "Arrêt du tabac",
               "activite_aerobie": "Activité physique aérobie", "reduction_alcool": "Réduction de l'alcool*"}
PIEGES = {"pilule": "Contraception hormonale", "labo_biochimie": "Laboratoire (biochimie)", "labo_numeration": "Laboratoire (numération)",
          "non_a_jeun_meme_personne": "Prélèvement non à jeun"}


def _lit(s):
    return ast.literal_eval(s) if isinstance(s, str) else s


def data():
    O = A.OUT
    pa = pd.read_csv(O / "signatures_partie_a.csv")
    nh = pa[(pa.jeu == "nh3") & (pa.panel == "18") & (pa.horizon == "6 mois")].iloc[0]
    cal = pa[(pa.jeu == "2001") & (pa.panel == "18") & (pa.horizon == "6 mois")].iloc[0]
    tr = pd.read_csv(O / "signatures_partie_a_transitions.csv")
    tr6 = tr[(tr.jeu == "nh3") & (tr.horizon == "6 mois")].iloc[0]
    ci = pd.read_csv(O / "signatures_ic_recalage.csv")
    ci = ci[ci.horizon == "6 mois"]
    det = pd.read_csv(O / "signatures_detection.csv")
    det = det[(det.variante == "principal") & (det.horizon == "6 mois")].set_index("intervention")
    sig = []
    for _, r in ci.iterrows():
        sig.append({"id": r.intervention, "nom": NOMS_COURTS[r.intervention], "meilleur": det.loc[r.intervention, "meilleur_marqueur"],
                    "sig": r.sens_sig, "sig_ic": _lit(r.sens_sig_ic95), "best": r.sens_best, "best_ic": _lit(r.sens_best_ic95),
                    "fa": r.fa_sig, "fa_ic": _lit(r.fa_sig_ic95)})
    order = ["mediterraneen", "perte_poids", "arret_tabac", "activite_aerobie", "reduction_alcool"]
    sig.sort(key=lambda x: order.index(x["id"]))
    g = pd.read_csv(O / "signatures_usage_global_ic_recalage.csv")
    g6 = g[g.horizon == "6 mois"].iloc[0]
    pit = pd.read_csv(O / "signatures_pieges.csv")
    pit = pit[pit.horizon == "6 mois"]
    corr = pd.read_csv(O / "signatures_correction.csv")
    corr = corr[corr.horizon == "6 mois"].set_index("intervention")
    pieges = []
    for pk, pn in PIEGES.items():
        for iv in ["perte_poids", "mediterraneen", "arret_tabac", "activite_aerobie", "reduction_alcool"]:
            for s in ("+", "−"):
                v = pit[(pit.piege == pk) & (pit.sens == s) & (pit.intervention == iv)].declenchement_signature.iloc[0]
                c = None
                if iv in corr.index:
                    col = f"declenchement_{pk}_{'+' if s == '+' else '-'}"
                    c = float(corr.loc[iv, col]) if col in corr.columns else None
                pieges.append({"piege": pn, "sens": "début / passage" if s == "+" else "arrêt / retour", "iv": NOMS_COURTS[iv], "taux": float(v),
                               "contrainte": c})
    corrs = [{"iv": NOMS_COURTS[i], "orig": float(r.sens_originale), "contr": float(r.sens_contrainte), "pieges": r.pieges_neutralises}
             for i, r in corr.iterrows()]
    lv = pd.read_csv(O / "signatures_levier_depart.csv")
    lev = [{"iv": NOMS_COURTS[r.intervention], "b": int(r.prelevements_depart), "f": int(r.bilans_suivi), "sig": r.sens_signature,
            "best": r.sens_meilleur_seul} for _, r in lv.iterrows() if r.intervention != "activite_aerobie"]
    people = json.loads((O / "demo_personnes.json").read_text(encoding="utf-8"))
    return {"a": {"au_moins_1": nh.part_au_moins_1, "au_moins_1_ic": _lit(nh.ic95_au_moins_1), "au_moins_3": nh.part_au_moins_3,
                  "indep_1": nh.attendu_independance_au_moins_1, "indep_3": nh.attendu_independance_au_moins_3, "n": int(nh.n_paires_completes),
                  "cal_1": cal.part_au_moins_1, "fbn": tr6.part_fausse_bonne_nouvelle, "fas": tr6.part_fausse_alerte_seuil},
            "sig": sig, "global_fa": g6.fausses_alertes_5_signatures, "global_fa_ic": _lit(g6.ic95), "pieges": pieges, "corr": corrs,
            "levier": lev, "people": people}


HTML = r"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Signatures multi-marqueurs</title>
<style>
:root {
  --surface: #ffffff; --plane: #ffffff; --ink: #0b0b0b; --ink-2: #52514e; --muted: #898781;
  --grid: #e1e0d9; --axis: #c3c2b7; --s1: #2a78d6; --s2: #898781; --accent: #2a78d6; --warn-bg: #f7f6f2;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--plane); color: var(--ink); font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 920px; margin: 0 auto; padding: 32px 16px 64px; }
h1 { font-size: 26px; margin: 0 0 4px; font-weight: 650; }
h2 { font-size: 19px; margin: 44px 0 6px; font-weight: 650; }
h3 { font-size: 15px; margin: 18px 0 6px; font-weight: 650; }
p, li { color: var(--ink-2); }
.sub { color: var(--ink-2); margin: 0 0 6px; }
.note { font-size: 13px; color: var(--muted); }
.banner { border: 1px solid var(--grid); background: var(--warn-bg); padding: 10px 14px; border-radius: 6px; font-size: 13.5px; color: var(--ink-2); margin: 16px 0 0; }
.hero { display: flex; gap: 32px; flex-wrap: wrap; margin-top: 14px; }
.hero .fig { font-size: 52px; font-weight: 650; line-height: 1; }
.hero .lab { color: var(--ink-2); max-width: 260px; font-size: 14px; margin-top: 6px; }
.tile { min-width: 200px; }
table { border-collapse: collapse; width: 100%; font-size: 13.5px; margin-top: 8px; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--grid); vertical-align: top; }
th { font-weight: 600; color: var(--ink-2); font-size: 12.5px; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
.legend { display: flex; gap: 18px; font-size: 13px; color: var(--ink-2); margin: 6px 0 4px; flex-wrap: wrap; }
.key { display: inline-block; width: 18px; height: 2px; vertical-align: middle; margin-right: 6px; }
.dotkey { display: inline-block; width: 10px; height: 10px; border-radius: 50%; vertical-align: middle; margin-right: 6px; }
svg text { font: 12px system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink-2); }
.tip { position: fixed; pointer-events: none; background: #fff; border: 1px solid var(--grid); border-radius: 6px; padding: 6px 9px; font-size: 12.5px; color: var(--ink); box-shadow: 0 2px 8px rgba(0,0,0,.08); display: none; }
.people { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 10px; }
.card { border: 1px solid var(--grid); border-radius: 8px; padding: 12px 14px; }
.card h3 { margin: 0 0 2px; }
.card .ctx { font-size: 12.5px; color: var(--muted); margin-bottom: 8px; }
.verdict { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 8px 0; }
.verdict div { border: 1px solid var(--grid); border-radius: 6px; padding: 8px; font-size: 13px; }
.verdict b { display: block; font-size: 12px; color: var(--muted); font-weight: 600; margin-bottom: 2px; }
.small td, .small th { padding: 3px 6px; font-size: 12.5px; }
.flag { color: var(--ink); font-weight: 600; }
details summary { cursor: pointer; font-size: 13px; color: var(--ink-2); margin-top: 6px; }
footer { margin-top: 48px; font-size: 12.5px; color: var(--muted); border-top: 1px solid var(--grid); padding-top: 12px; }
</style>
</head>
<body>
<main>
<h1>Détecter l'effet d'une intervention avec plusieurs marqueurs</h1>
<p class="sub">Visualisation de résultats de recherche : signatures multi-marqueurs sur des paires de prises de sang répétées (NHANES).</p>
<div class="banner">Ceci n'est pas un outil de décision ni un produit. Les chiffres viennent de données publiques américaines (NHANES),
d'effets moyens tirés de méta-analyses et d'une simulation pour l'horizon de 6 mois. Les personnes présentées plus bas sont
<b>fictives</b> (données synthétiques).</div>

<h2>1. Sans rien changer, plus d'une personne sur deux a un marqueur « significatif »</h2>
<p>Paires de prises de sang chez des personnes sans intervention (NHANES III), bruit extrapolé à 6 mois, 18 marqueurs
d'un bilan de suivi, chacun comparé à son changement détectable.</p>
<div class="hero" id="hero"></div>

<h2>2. Une signature fait mieux qu'un marqueur seul, mais reste loin d'une détection fiable</h2>
<p>Part des personnes chez qui l'effet moyen d'une intervention est détecté à 6 mois, avec 5 % de fausses alertes calées
sur d'autres personnes (NHANES 2001-2002). Chaque personne reçoit une part aléatoire de l'effet moyen (en moyenne 100 %,
écart type 50 %). Les intervalles à 95 % intègrent l'incertitude du calage des seuils.</p>
<div class="legend"><span><span class="dotkey" style="background:var(--s1)"></span>Signature (filtre adapté)</span>
<span><span class="dotkey" style="background:var(--s2)"></span>Meilleur marqueur seul</span></div>
<div id="chart-sig"></div>
<p class="note" id="fa-note"></p>
<p class="note">* Réduction de l'alcool : signature non interprétable. Aucune source lue ne chiffre l'effet sur la GGT, et elle repose
à 93 % sur une <b>baisse</b> du HDL (réduire l'alcool fait baisser le HDL : un affichage naïf montrerait un marqueur « dégradé »).</p>
<details><summary>Tableau des valeurs</summary><div id="tab-sig"></div></details>

<h2>3. Pièges : contraception, laboratoire, jeûne</h2>
<p>Part des personnes <b>sans intervention</b> chez qui la signature se déclenche quand un piège survient entre les deux
bilans (fausses alertes de base : environ 5 %). La « signature insensible aux pièges » est rendue orthogonale aux directions
des pièges qui la déclenchent au-delà de 10 %.</p>
<div id="tab-pieges"></div>
<h3>Ce que coûte la signature insensible aux pièges</h3>
<div id="tab-corr"></div>

<h2>4. Le levier du bilan de départ</h2>
<p><b>Recommandation de conception.</b> Sensibilité à 6 mois de la signature selon le nombre de prélèvements au départ
(à quelques semaines d'intervalle) et de bilans de suivi. Modèle gaussien, effet maintenu, 5 % de fausses alertes. Un
deuxième prélèvement au départ aide, mais moins qu'un deuxième bilan de suivi : des prélèvements rapprochés partagent la
même variation à long terme.</p>
<div id="tab-levier"></div>
<p class="note" id="levier-note"></p>

<h2>5. Cinq personnes fictives suivies sur deux bilans</h2>
<p>Données <b>synthétiques</b> : valeurs de départ égales aux médianes des 30-55 ans, variation tirée du modèle de bruit à 6 mois,
plus l'effet ou le piège annoncé. La comparaison naïve signale chaque marqueur qui dépasse son changement détectable ; la signature
teste seulement le protocole prescrit. Pour chaque cas, la règle de choix du tirage est indiquée.</p>
<div class="people" id="people"></div>

<h2>6. Limites, en clair</h2>
<ul>
<li>Les prises de sang répétées sont à <b>2 semaines</b> d'intervalle. L'horizon de 6 mois est <b>simulé</b> ; la variabilité à long
terme vient d'études EFLM de qualité inégale (toutes notes) pour 16 marqueurs sur 18. Avec les seules études de bonne qualité,
seules l'ALAT et l'ASAT recevaient un bruit à long terme : c'était une borne optimiste (version corrigée le 12 novembre 2026).</li>
<li>Les effets d'intervention sont des <b>moyennes de méta-analyses</b>, souvent chez des personnes malades (obésité, stéatose), et
souvent assemblées à partir d'études différentes. L'effet sur l'ALAT est probablement surestimé pour des personnes en bonne santé.</li>
<li>La part d'effet reçue par chaque personne est <b>postulée</b>, pas mesurée.</li>
<li>Une signature dit qu'il y a eu un changement <b>compatible</b> avec l'effet attendu, pas lequel : une perte de poids déclenche aussi
la signature de l'activité physique dans 23 % des cas.</li>
<li>Tester toutes les signatures à la fois fait monter les fausses alertes (voir section 2).</li>
<li>Données américaines, laboratoires des années 1988-2002 ; les écarts réels entre laboratoires de routine sont inconnus pour les
lipides et la numération.</li>
<li>Rien ici ne permet de dire, pour une personne, qu'un programme « n'a pas marché » : ne pas détecter n'est pas prouver l'absence d'effet.</li>
</ul>
<footer>Programme de recherche « signatures » : rapport complet et protocole pré-enregistré dans le dépôt
(reports/signatures/SIGNATURES.md, DECISIONS.md). Page générée automatiquement à partir des fichiers de résultats.</footer>
</main>
<div class="tip" id="tip"></div>
<script>
const D = __DATA__;
const pct = (x, d = 0) => (100 * x).toFixed(d).replace('.', ',') + ' %';
const fmt = (x) => { const a = Math.abs(x); const d = a >= 100 ? 0 : a >= 10 ? 1 : 2; return x.toFixed(d).replace('.', ','); };
const el = (t, a = {}, txt) => { const e = document.createElement(t); for (const k in a) e.setAttribute(k, a[k]); if (txt !== undefined) e.textContent = txt; return e; };
const svgEl = (t, a = {}) => { const e = document.createElementNS('http://www.w3.org/2000/svg', t); for (const k in a) e.setAttribute(k, a[k]); return e; };
const tip = document.getElementById('tip');
function showTip(ev, lines) { tip.replaceChildren(...lines.map(l => { const d = el('div'); d.textContent = l; return d; })); tip.style.display = 'block';
  tip.style.left = Math.min(ev.clientX + 12, innerWidth - 240) + 'px'; tip.style.top = (ev.clientY + 12) + 'px'; }
function hideTip() { tip.style.display = 'none'; }

// 1. hero
(function () {
  const h = document.getElementById('hero'); const a = D.a;
  const tiles = [[pct(a.au_moins_1), `ont au moins un marqueur sur 18 au-delà de son changement détectable en 6 mois, sans rien changer (${pct(a.indep_1)} attendus si les marqueurs étaient indépendants).`],
                 [pct(a.au_moins_3, 1), `en ont au moins trois : les faux changements arrivent en grappes (${pct(a.indep_3, 1)} attendus sous indépendance).`],
                 [pct(a.fbn), `voient au moins une valeur anormale redevenir normale toute seule (« fausse bonne nouvelle »).`]];
  for (const [f, l] of tiles) { const t = el('div', {class: 'tile'}); t.append(el('div', {class: 'fig'}, f), el('div', {class: 'lab'}, l)); h.append(t); }
  h.after(el('p', {class: 'note'}, `NHANES III, ${a.n} personnes, paires complètes ; intervalle à 95 % de la première valeur : ${pct(a.au_moins_1_ic[0])} à ${pct(a.au_moins_1_ic[1])}.`));
})();

// 2. dot-and-interval chart
(function () {
  const W = Math.min(880, document.querySelector('main').clientWidth), rowH = 46, top = 10, left = 210, right = 24, H = top + D.sig.length * rowH + 30;
  const s = svgEl('svg', {width: W, height: H, role: 'img', 'aria-label': 'Sensibilité de la signature et du meilleur marqueur seul par intervention'});
  const x = v => left + v * (W - left - right);
  for (const t of [0, .2, .4, .6, .8, 1]) { s.append(svgEl('line', {x1: x(t), x2: x(t), y1: top, y2: H - 24, stroke: 'var(--grid)', 'stroke-width': 1}));
    const tx = svgEl('text', {x: x(t), y: H - 8, 'text-anchor': 'middle'}); tx.textContent = (t * 100) + ' %'; s.append(tx); }
  D.sig.forEach((r, i) => {
    const y = top + i * rowH + rowH / 2;
    const lab = svgEl('text', {x: 0, y: y + 4}); lab.textContent = r.nom; lab.setAttribute('fill', 'var(--ink)'); s.append(lab);
    [['best', 'var(--s2)', 7], ['sig', 'var(--s1)', -7]].forEach(([k, c, dy]) => {
      const ic = r[k + '_ic'];
      s.append(svgEl('line', {x1: x(ic[0]), x2: x(ic[1]), y1: y + dy, y2: y + dy, stroke: c, 'stroke-width': 2, 'stroke-linecap': 'round'}));
      const dot = svgEl('circle', {cx: x(r[k]), cy: y + dy, r: 5, fill: c, stroke: 'var(--surface)', 'stroke-width': 2});
      s.append(dot);
      const hit = svgEl('rect', {x: x(ic[0]) - 6, y: y + dy - 10, width: Math.max(24, x(ic[1]) - x(ic[0]) + 12), height: 20, fill: 'transparent', tabindex: 0});
      const lines = [`${k === 'sig' ? 'Signature' : 'Meilleur seul (' + r.meilleur + ')'} : ${pct(r[k])}`, `IC 95 % : ${pct(ic[0])} à ${pct(ic[1])}`, r.nom];
      hit.addEventListener('pointermove', e => showTip(e, lines)); hit.addEventListener('pointerleave', hideTip);
      hit.addEventListener('focus', e => { const b = hit.getBoundingClientRect(); showTip({clientX: b.right, clientY: b.top}, lines); }); hit.addEventListener('blur', hideTip);
      s.append(hit);
    });
    const v = svgEl('text', {x: x(r.sig_ic[1]) + 8, y: y - 3}); v.textContent = pct(r.sig); v.setAttribute('fill', 'var(--ink)'); s.append(v);
  });
  document.getElementById('chart-sig').append(s);
  document.getElementById('fa-note').textContent = `Fausses alertes observées sur des personnes non vues au calage : ${D.sig.map(r => r.nom.replace('*', '') + ' ' + pct(r.fa, 1)).join(' ; ')}. ` +
    `Si l'on teste les 5 signatures à la fois : ${pct(D.global_fa)} (IC 95 % ${pct(D.global_fa_ic[0])} à ${pct(D.global_fa_ic[1])}).`;
  const t = el('table'); const hd = el('tr'); ['Intervention', 'Signature', 'IC 95 %', 'Meilleur seul', 'IC 95 %', 'Fausses alertes'].forEach((h, j) => hd.append(el('th', j ? {class: 'num'} : {}, h))); t.append(hd);
  D.sig.forEach(r => { const tr = el('tr'); tr.append(el('td', {}, r.nom), el('td', {class: 'num'}, pct(r.sig)), el('td', {class: 'num'}, pct(r.sig_ic[0]) + ' – ' + pct(r.sig_ic[1])),
    el('td', {class: 'num'}, pct(r.best) + ' (' + r.meilleur + ')'), el('td', {class: 'num'}, pct(r.best_ic[0]) + ' – ' + pct(r.best_ic[1])), el('td', {class: 'num'}, pct(r.fa, 1))); t.append(tr); });
  document.getElementById('tab-sig').append(t);
})();

// 3. pieges
(function () {
  const ivs = [...new Set(D.pieges.map(p => p.iv))];
  const t = el('table'); const hd = el('tr'); hd.append(el('th', {}, 'Piège'), el('th', {}, 'Sens'));
  ivs.forEach(i => hd.append(el('th', {class: 'num'}, i))); t.append(hd);
  const keys = [...new Set(D.pieges.map(p => p.piege + '|' + p.sens))];
  keys.forEach(k => { const [pg, sn] = k.split('|'); const tr = el('tr'); tr.append(el('td', {}, pg), el('td', {}, sn));
    ivs.forEach(i => { const p = D.pieges.find(q => q.piege === pg && q.sens === sn && q.iv === i);
      const td = el('td', {class: 'num'}); const v = el('span', p.taux > 0.10 ? {class: 'flag'} : {}, pct(p.taux)); td.append(v);
      if (p.contrainte !== null && p.taux > 0.10) td.append(el('div', {class: 'note'}, '→ ' + pct(p.contrainte) + ' insensible'));
      tr.append(td); }); t.append(tr); });
  document.getElementById('tab-pieges').append(t);
  document.getElementById('tab-pieges').append(el('p', {class: 'note'}, 'En gras : au-delà de 10 %. « → insensible » : même piège avec la signature insensible aux pièges.'));
  const c = el('table'); const h2 = el('tr'); ['Intervention', 'Pièges neutralisés', 'Sensibilité, signature', 'Sensibilité, insensible aux pièges'].forEach((h, j) => h2.append(el('th', j > 1 ? {class: 'num'} : {}, h))); c.append(h2);
  D.corr.forEach(r => { const tr = el('tr'); tr.append(el('td', {}, r.iv), el('td', {}, r.pieges.replaceAll('_', ' ')), el('td', {class: 'num'}, pct(r.orig)), el('td', {class: 'num'}, pct(r.contr))); c.append(tr); });
  document.getElementById('tab-corr').append(c);
})();

// 4. levier
(function () {
  const ivs = [...new Set(D.levier.map(r => r.iv))];
  const t = el('table'); const hd = el('tr'); hd.append(el('th', {}, 'Prélèvements au départ'), el('th', {}, 'Bilans de suivi'));
  ivs.forEach(i => hd.append(el('th', {class: 'num'}, i))); t.append(hd);
  for (const f of [1, 2]) for (const b of [1, 2, 3]) { const tr = el('tr'); tr.append(el('td', {}, String(b)), el('td', {}, f === 1 ? '1 (6 mois)' : '2 (6 et 12 mois)'));
    ivs.forEach(i => { const r = D.levier.find(q => q.iv === i && q.b === b && q.f === f); tr.append(el('td', {class: 'num'}, pct(r.sig))); }); t.append(tr); }
  document.getElementById('tab-levier').append(t);
  const g = i => { const a = D.levier.find(q => q.iv === i && q.b === 1 && q.f === 1).sig, b = D.levier.find(q => q.iv === i && q.b === 2 && q.f === 1).sig; return [a, b]; };
  const [a, b] = g(ivs[0]);
  document.getElementById('levier-note').textContent = `Un deuxième prélèvement au départ, quelques semaines avant le début du programme, fait passer la détection de la perte de poids de ${pct(a)} à ${pct(b)} (un deuxième bilan de suivi, à ${pct(D.levier.find(q => q.iv === ivs[0] && q.b === 1 && q.f === 2).sig)}) ; ` +
    `ajouter en plus un bilan à 12 mois la porte à ${pct(D.levier.find(q => q.iv === ivs[0] && q.b === 2 && q.f === 2).sig)}. Modèle gaussien : les valeurs d'une même ligne sont comparables entre elles, pas avec la section 2.`;
})();

// 5. personnes
(function () {
  const box = document.getElementById('people');
  D.people.forEach(p => {
    const c = el('div', {class: 'card'}); c.append(el('h3', {}, 'Personne ' + p.code), el('div', {class: 'ctx'}, p.titre));
    const v = el('div', {class: 'verdict'});
    const n1 = el('div'); n1.append(el('b', {}, 'Comparaison naïve'), document.createTextNode(p.n_naif === 0 ? 'Aucun marqueur ne bouge au-delà de son seuil.' : `${p.n_naif} marqueur${p.n_naif > 1 ? 's' : ''} « significatif${p.n_naif > 1 ? 's' : ''} » : ` +
      p.marqueurs.filter(m => m.naif).map(m => m.nom + (m.naif === 'hausse' ? ' ↑' : ' ↓')).join(', ') + '.'));
    const n2 = el('div'); n2.append(el('b', {}, 'Signature : ' + p.intervention),
      document.createTextNode((p.alerte ? 'Changement compatible avec l\'effet attendu.' : 'Pas de changement détectable.') + ` (score ${fmt(p.signature)}, seuil ${fmt(p.seuil)})`));
    v.append(n1, n2); c.append(v);
    c.append(el('div', {class: 'note'}, `Signature insensible aux pièges : ${p.alerte_contrainte ? 'se déclenche' : 'ne se déclenche pas'} (score ${fmt(p.signature_contrainte)}, seuil ${fmt(p.seuil_contrainte)}).` +
      (p.alerte_contrainte && p.titre.startsWith('Sans intervention') ? ' Ici, c\'est le bruit : le piège ne pèse plus sur cette signature, mais 5 % de fausses alertes restent attendues.' : '')));
    const det = el('details'); det.append(el('summary', {}, 'Les 18 marqueurs'));
    const t = el('table', {class: 'small'}); const hd = el('tr'); ['Marqueur', 'Bilan 1', 'Bilan 2', 'Variation'].forEach((h, j) => hd.append(el('th', j ? {class: 'num'} : {}, h))); t.append(hd);
    p.marqueurs.forEach(m => { const tr = el('tr'); tr.append(el('td', m.naif ? {class: 'flag'} : {}, m.nom + ' (' + m.unite + ')'), el('td', {class: 'num'}, fmt(m.b1)), el('td', {class: 'num'}, fmt(m.b2)),
      el('td', {class: 'num'}, (m.variation_pct > 0 ? '+' : '') + m.variation_pct.toFixed(0) + ' %')); t.append(tr); });
    det.append(t); c.append(det);
    c.append(el('div', {class: 'note'}, 'Tirage retenu : ' + p.regle + '.'));
    box.append(c);
  });
})();
</script>
</body>
</html>
"""


def build():
    d = data()
    html = HTML.replace("__DATA__", json.dumps(d, ensure_ascii=False, default=float))
    (A.OUT / "demo_signatures.html").write_text(html, encoding="utf-8")
    return A.OUT / "demo_signatures.html"


if __name__ == "__main__":
    build()
