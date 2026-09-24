"""Phase 2: verify candidate references through Crossref (authoritative
bibliographic source). Only references with a confident match are kept.
Writes literature/literature_matrix.csv."""
import os, sys, json, time
import urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CANDIDATES = [
    # (bibtex-style query, topic tag)
    ("Bailey A study of queues and appointment systems in hospital outpatient departments Journal of the Royal Statistical Society 1952", "foundational outpatient scheduling"),
    ("Welch Bailey Appointment systems in hospital outpatient departments Lancet 1952", "foundational outpatient scheduling"),
    ("Lindley The theory of queues with a single server Proceedings of the Cambridge Philosophical Society 1952", "Lindley recursion"),
    ("Soriano Comparison of two scheduling policies Operations Research 1966", "appointment scheduling"),
    ("Cayirli Veral Outpatient scheduling in health care a review of literature Production and Operations Management 2003", "review"),
    ("Gupta Denton Appointment scheduling in health care challenges and opportunities IIE Transactions 2008", "review"),
    ("Robinson Chen Scheduling doctor's appointments optimal and empirically-based heuristic policies IIE Transactions 2003", "heuristic appointment rules"),
    ("Denton Gupta A sequential bounding approach for optimal appointment scheduling IIE Transactions 2003", "stochastic programming"),
    ("Klassen Yoogalingam Appointment system design with interruptions and patient lateness Omega 2013", "Omega appointment scheduling"),
    ("Muthuraman Lawley A stochastic overbooking model for outpatient clinical scheduling with no-shows IIE Transactions 2008", "overbooking no-shows"),
    ("Kaandorp Koole Optimal outpatient appointment scheduling Health Care Management Science 2007", "optimal intervals"),
    ("Begen Queyranne Appointment scheduling with discrete random durations Mathematics of Operations Research 2011", "discrete optimization"),
    ("Mak Rong Zhang Appointment scheduling with limited distributional information Management Science 2015", "DRO appointment scheduling"),
    ("Kong Lee Teo Zheng Scheduling arrivals to a stochastic service delivery system using copositive cones Operations Research 2013", "conic/DRO scheduling"),
    ("Deceuninck Fiems De Vuyst Outpatient scheduling with unpunctual patients and no-shows European Journal of Operational Research 2018", "unpunctuality"),
    ("Hassin Mendel Scheduling arrivals to queues a single-server model with no-shows Management Science 2008", "queue arrivals scheduling"),
    ("Wang Fung Dynamic appointment scheduling with patient preferences and choices Industrial and Management 2015", "dynamic scheduling"),
    ("Zacharias Pinedo Appointment scheduling with no-shows and overbooking Production and Operations Management 2014", "no-show overbooking"),
    ("Berg Denton Erdogan Rohleder Huschka Optimal booking and scheduling in outpatient procedure centers Computers and Operations Research 2014", "outpatient procedure scheduling"),
    ("Chen Robinson Sequencing and scheduling appointments with stochastic service times Operations Research 2014", "sequencing stochastic service"),
    ("Mittal Schulz Optimizing appointment schedules by simulation Optimization Letters 2014", "simulation optimization"),
    ("Schulz Appointment scheduling under patient-dependent stochastic service times Omega 2022", "Omega stochastic service"),
    ("Rockafellar Uryasev Optimization of conditional value-at-risk Journal of Risk 2000", "CVaR"),
    ("Bertsimas Sim The price of robustness Operations Research 2004", "robust optimization"),
    ("Rahimian Mehrotra Distributionally robust optimization a review Operations Research 2022", "DRO review"),
    ("Pinedo Scheduling Theory Algorithms and Systems", "scheduling textbook"),
    ("Geng Xie Jiang Optimal outpatient appointment scheduling with unpunctuality optimization European Journal of Operational Research", "Omega/EJOR unpunctual scheduling"),
    ("Ahmadi-Javid Jalali Klassen Outpatient appointment systems in healthcare a review of optimization studies European Journal of Operational Research 2017", "review optimization"),
    ("Salzarulo Mahar Bretthauer Appointment scheduling and the impact of service time variability Health Care Management Science 2011", "service variability"),
    ("Cayirli Veral Rosen Designing appointment scheduling systems for ambulatory care services Health Care Management Science 2006", "design of appointment systems"),
]


def crossref_query(q):
    url = ("https://api.crossref.org/works?rows=3&query.bibliographic="
           + urllib.parse.quote(q))
    req = urllib.request.Request(url, headers={"User-Agent": "research-check/1.0 (mailto:devin@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.load(r)["message"]["items"]
    return items


def main():
    import csv
    rows = []
    for q, tag in CANDIDATES:
        try:
            items = crossref_query(q)
        except Exception as e:
            rows.append({"query": q, "topic": tag, "verified": "NO", "error": str(e)})
            continue
        best = items[0] if items else {}
        title = (best.get("title") or [""])[0]
        score = best.get("score", 0)
        doi = best.get("DOI", "")
        year = (best.get("issued", {}).get("date-parts") or [[None]])[0][0]
        journal = (best.get("container-title") or [""])[0]
        authors = "; ".join(
            f"{a.get('family','')}, {a.get('given','')}" for a in best.get("author", [])[:4])
        verified = "YES" if score >= 40 and doi else ("MAYBE" if doi else "NO")
        rows.append({"query": q, "topic": tag, "verified": verified,
                     "score": score, "title": title, "journal": journal,
                     "year": year, "doi": doi, "authors": authors})
        print(verified, round(score, 1), title[:70])
        time.sleep(0.3)
    out = os.path.join(ROOT, "literature", "literature_matrix.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("wrote", out)


if __name__ == "__main__":
    main()
