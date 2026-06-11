"""Build script for belumbayar 2-page redesign"""
import re, sys

path = r'C:\Users\irgir\belumbayar-repo\index.html'
out  = r'C:\Users\irgir\belumbayar-repo\index_new.html'

with open(path, 'r', encoding='utf-8') as f:
    old = f.read()

def extract_fn(name, src=old):
    idx = src.find(f'function {name}')
    if idx < 0:
        for p in ['let ', 'const ']:
            idx = src.find(f'{p}{name}')
            if idx >= 0: break
    if idx < 0: return ''
    brace = src.find('{', idx)
    if brace < 0: return ''
    bc, started = 0, False
    for i in range(brace, len(src)):
        if src[i] == '{': bc += 1; started = True
        elif src[i] == '}': bc -= 1
        if started and bc == 0: return src[idx:i+1]
    return ''

fnames = ['getDusun','getDusunLabel','rp','autoAlamat','tgl','nomorFmt',
          'animateCounter','filterDusun','onDusunSelect','populateRwByDusun',
          'onRwSelect','updateRtOptions','applyFilter','renderTable',
          'renderPagination','goPage','togglePilih','pilihSemua',
          'updatePilihan','bukaModal','tutupModal','rerender',
          'htmlPemberitahuan','htmlUndangan','buildSuratCetak','docetak','cetakBatch']
fns = {n: extract_fn(n) for n in fnames}

state_s = old[old.find('// ============ STATE'):old.find('// ============ UTILS')]
data_s  = old[old.find('const PBB_DATA'):old.find('const PBB_DATA')+80000]
dusun_s = old[old.find('const DUSUN_RW'):old.find('function getDusun')]

new_html = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard PBB — Desa Kasomalang Kulon</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--h: #1a5c3a;--ht:#0f3a25;--hm:#e8f4ee;--e:#c49a28;--em:#fdf8e8;--t:#1a1a1a;--a:#6b7280;--b:#d1d5db;--m:#dc2626}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f0f4f0;color:var(--t);min-height:100vh}
/* NAVBAR */
.nb{background:var(--ht);color:#fff;border-bottom:4px solid var(--e);position:sticky;top:0;z-index:100}
.nbi{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;gap:16px}
.nbl{width:44px;height:44px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.nbt h1{font-size:0.95rem;font-weight:700}
.nbt p{font-size:0.72rem;color:#a7c4b5}
.nbb{margin-left:auto;background:var(--e);color:var(--ht);padding:4px 12px;border-radius:20px;font-size:0.72rem;font-weight:700;white-space:nowrap}
.nt{display:flex;border-top:1px solid rgba(255,255,255,.1)}
.nv{padding:10px 28px;cursor:pointer;font-size:0.82rem;font-weight:600;color:rgba(255,255,255,.6);border-bottom:3px solid transparent;transition:all .15s;text-align:center;position:relative}
.nv:hover{color:#fff;background:rgba(255,255,255,.06)}
.nv.aktif{color:#fff;border-bottom-color:var(--e);background:rgba(255,255,255,.08)}
.nv span{display:block;font-size:0.68rem;opacity:.7}
/* PAGES */
.pg{display:none}.pg.ak{display:block}
.pd{max-width:1200px;margin:0 auto;padding:24px}
/* HERO BIG */
.hb{background:linear-gradient(135deg,var(--ht) 0%,#1a5c3a 50%,#0f3a25 100%);border-radius:16px;padding:36px 40px;color:#fff;position:relative;overflow:hidden;margin-bottom:24px}
.hb::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");}
.hl{font-size:0.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--e);margin-bottom:8px;display:flex;align-items:center;gap:8px}
.ha{font-size:clamp(2.4rem,6vw,4rem);font-weight:900;line-height:1;color:#fff;letter-spacing:-2px;position:relative}
.hs{font-size:0.8rem;color:rgba(255,255,255,.55);margin-top:8px;position:relative}
.hbr{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:24px;position:relative}
.hbs{background:rgba(255,255,255,.08);border-radius:10px;padding:12px 14px}
.hbsn{font-size:1.2rem;font-weight:800;color:var(--e);line-height:1}
.hbsl{font-size:0.68rem;color:rgba(255,255,255,.55);margin-top:3px}
/* SECTION TITLE */
.st{font-size:0.75rem;font-weight:700;color:var(--ht);text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.st::after{content:'';flex:1;height:1px;background:var(--b)}
/* DUSUN CARDS */
.dg{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:24px}
.dc{background:#fff;border-radius:12px;padding:18px 16px;box-shadow:0 1px 4px rgba(0,0,0,.07);cursor:pointer;transition:all .2s;border:2px solid transparent;position:relative;overflow:hidden}
.dc::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:var(--h)}
.dc:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.12)}
.dc.ak{border-color:var(--h)}
.dc.ak::before{background:var(--e)}
.dc.lu::before{background:#888}
.di{font-size:1.6rem;margin-bottom:8px}
.dn{font-size:0.78rem;font-weight:700;color:var(--ht)}
.dr{font-size:0.68rem;color:var(--a);margin-top:2px}
.dc2{font-size:1.5rem;font-weight:900;color:var(--ht);margin-top:10px;line-height:1}
.dt{font-size:0.78rem;font-weight:700;color:var(--m);margin-top:4px}
.dbr{height:6px;background:#e8f4ee;border-radius:3px;margin-top:10px;overflow:hidden}
.dbf{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--h),var(--e));transition:width 1s ease}
/* CHARTS */
.cr{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px}
.cc{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.07)}
.ct{font-size:0.78rem;font-weight:700;color:var(--ht);text-transform:uppercase;letter-spacing:.5px;margin-bottom:16px}
.bc{display:flex;flex-direction:column;gap:8px}
.br{display:flex;align-items:center;gap:10px}
.bl{font-size:0.75rem;font-weight:600;color:var(--a);min-width:44px;text-align:right}
.bt{flex:1;height:22px;background:#f0f4f1;border-radius:6px;overflow:hidden}
.bf{height:100%;border-radius:6px;display:flex;align-items:center;padding-left:8px;font-size:0.68rem;font-weight:700;color:#fff;white-space:nowrap;min-width:40px;transition:width 1.2s ease}
.bf.h{background:linear-gradient(90deg,#1a5c3a,#2e8b57)}
.bf.e{background:linear-gradient(90deg,#c49a28,#e0b84a)}
.bf.m{background:linear-gradient(90deg,#dc2626,#ef4444)}
.bf.u{background:linear-gradient(90deg,#7c3aed,#a78bfa)}
.bf.a2{background:linear-gradient(90deg,#555,#888)}
.bv{font-size:0.7rem;font-weight:600;color:var(--t);min-width:70px}
/* TOP DEBTORS */
.td{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.07)}
.tdh{background:var(--ht);color:#fff;padding:12px 20px;font-size:0.8rem;font-weight:700;display:flex;align-items:center;justify-content:space-between}
.tl{padding:0}
.ti{display:flex;align-items:center;gap:12px;padding:10px 20px;border-bottom:1px solid #f0f0f0;transition:background .1s}
.ti:last-child{border-bottom:none}
.ti:hover{background:var(--hm)}
.tr2{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:800;flex-shrink:0}
.tr2.g{background:#fff3cd;color:#92700c}
.tr2.s{background:#f0f0f0;color:#666}
.tr2.b{background:#fee2e2;color:#b91c1c}
.tr2.n{background:var(--hm);color:var(--ht)}
.ti2{flex:1}
.tn{font-size:0.84rem;font-weight:700}
.tm{font-size:0.7rem;color:var(--a);margin-top:1px}
.ta{font-size:0.9rem;font-weight:800;color:var(--m)}
/* PAGE 2 */
.pdm{max-width:1200px;margin:0 auto;padding:24px}
.pc{background:#fff;border-radius:12px;padding:20px;margin-bottom:20px;box-shadow:0 1px 4px rgba(0,0,0,.07)}
.pc h2{font-size:0.8rem;font-weight:700;color:var(--ht);text-transform:uppercase;letter-spacing:.8px;margin-bottom:12px}
.fr{display:flex;gap:10px;flex-wrap:wrap}
.fr input,.fr select{flex:1;min-width:140px;padding:9px 13px;border:1.5px solid var(--b);border-radius:8px;font-size:0.88rem;font-family:inherit;outline:none;background:#fff}
.fr input:focus,.fr select:focus{border-color:var(--h)}
.fab{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:10px;font-size:0.8rem;color:var(--a)}
.pt{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.07);margin-bottom:24px}
.th{background:var(--h);color:#fff;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.th span{font-size:0.85rem;font-weight:600}
.tt{background:rgba(255,255,255,.2);padding:4px 12px;border-radius:12px;font-size:0.78rem}
.bc2{background:var(--e);color:var(--ht);border:none;padding:7px 16px;border-radius:7px;font-size:0.8rem;font-weight:700;cursor:pointer}
.bc2.hijau{background:rgba(255,255,255,.15);color:#fff;border:1px solid rgba(255,255,255,.3)}
.bc2:hover{opacity:.85}
.ts{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:0.84rem}
thead th{background:#f0f4f1;padding:10px 14px;text-align:left;font-weight:700;color:var(--ht);font-size:0.73rem;text-transform:uppercase;letter-spacing:.5px;border-bottom:2px solid var(--b);white-space:nowrap}
thead th:first-child{width:40px;text-align:center}
tbody tr{border-bottom:1px solid #f0f0f0;transition:background .1s;cursor:pointer}
tbody tr:hover{background:var(--hm)}
tbody tr.dp{background:#dff0e8}
td{padding:9px 14px;vertical-align:middle}
td:first-child{text-align:center}
td.nama{font-weight:600}
td.nop{font-family:monospace;font-size:0.77rem;color:var(--a)}
td.total{font-weight:700;color:var(--m)}
.badge-rt{background:#e8f4ee;color:var(--h);padding:2px 8px;border-radius:10px;font-size:0.73rem;font-weight:600;white-space:nowrap}
.badge-dusun{background:#fff3cd;color:#856404;padding:2px 7px;border-radius:8px;font-size:0.7rem;font-weight:600;margin-left:4px}
.yt{display:flex;gap:4px;flex-wrap:wrap}
.yt2{background:#fff3cd;color:#856404;padding:2px 7px;border-radius:8px;font-size:0.7rem;font-weight:600}
.ab{display:flex;gap:6px}
.bp,.bu{border:none;padding:5px 10px;border-radius:6px;font-size:0.73rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:all .15s}
.bp{background:var(--hm);color:var(--ht)}
.bp:hover{background:var(--h);color:#fff}
.bu{background:var(--em);color:#7a5f00}
.bu:hover{background:var(--e);color:var(--ht)}
input[type=checkbox]{width:15px;height:15px;cursor:pointer;accent-color:var(--h)}
.es{text-align:center;padding:48px;color:var(--a)}
.pg2{display:flex;align-items:center;justify-content:center;gap:6px;padding:14px;border-top:1px solid var(--b);flex-wrap:wrap}
.pg2 button{background:#fff;border:1.5px solid var(--b);padding:5px 12px;border-radius:6px;cursor:pointer;font-size:0.82rem;transition:all .15s}
.pg2 button:hover:not(:disabled){border-color:var(--h);color:var(--h)}
.pg2 button:disabled{opacity:.35;cursor:not-allowed}
.pg2 button.ak{background:var(--h);color:#fff;border-color:var(--h)}
.pg2 .ip{font-size:0.8rem;color:var(--a)}
/* MODALS */
.ov{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:200;padding:20px;overflow-y:auto}
.ov.ak{display:flex;align-items:flex-start;justify-content:center}
.md{background:#fff;border-radius:14px;width:100%;max-width:1000px;box-shadow:0 24px 80px rgba(0,0,0,.35);display:flex;flex-direction:column;max-height:calc(100vh - 40px);margin:auto;overflow:hidden}
.mh{background:var(--ht);color:#fff;padding:16px 22px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.mh.und{background:#6b3a00}
.mh h3{font-size:0.95rem;font-weight:700}
.mh button{background:none;border:none;color:#fff;font-size:1.5rem;cursor:pointer;line-height:1;opacity:.7}
.mh button:hover{opacity:1}
.mb{display:grid;grid-template-columns:300px 1fr;flex:1;overflow:hidden;min-height:0}
.mfc{padding:20px;border-right:1px solid var(--b);overflow-y:auto;display:flex;flex-direction:column;gap:14px}
.mpc{display:flex;flex-direction:column;background:#eef0ee;overflow:hidden}
.ptb{padding:9px 16px;background:#e0e4e0;border-bottom:1px solid #ccc;font-size:0.73rem;font-weight:700;color:#555;text-transform:uppercase;letter-spacing:.6px;flex-shrink:0}
.pb2{flex:1;overflow-y:auto;padding:20px}
.kp{background:#fff;box-shadow:0 3px 16px rgba(0,0,0,.15);border-radius:3px;padding:32px 36px;font-family:'Times New Roman',serif;font-size:10.5pt;line-height:1.6;color:#111;min-height:600px}
.kp .kop{text-align:center;border-bottom:3px double #111;padding-bottom:10px;margin-bottom:14px}
.kp .kop-nama{font-size:13.5pt;font-weight:bold;text-transform:uppercase}
.kp .kop-sub{font-size:10pt}
.kp .judul{text-align:center;font-size:12pt;font-weight:bold;text-decoration:underline;text-transform:uppercase;margin:12px 0 3px}
.kp .nomor{text-align:center;font-size:10pt;margin-bottom:16px}
.kp .ti2{border-collapse:collapse;margin-bottom:14px;width:auto}
.kp .ti2 td{padding:2px 0;font-size:10.5pt;vertical-align:top}
.kp .ti2 td:nth-child(2){padding:0 8px}
.kp .para{margin-bottom:10px;font-size:10.5pt;text-align:justify}
.kp .nominal{text-align:center;font-size:13pt;font-weight:bold;margin:10px 0 6px}
.kp .nominal-kecil{text-align:center;font-size:9pt;color:#444;margin-bottom:12px}
.kp .ttd2{display:flex;justify-content:flex-end;margin-top:20px}
.kp .ttd-box{text-align:center;min-width:200px}
.kp .ttd-jabatan{font-weight:bold}
.kp .ttd-spasi{height:58px}
.kp .ttd-nama{font-weight:bold;text-decoration:underline}
.fg{display:flex;flex-direction:column;gap:5px}
.fg label{font-size:0.77rem;font-weight:700;color:var(--ht);text-transform:uppercase;letter-spacing:.5px}
.fg input{padding:8px 12px;border:1.5px solid var(--b);border-radius:7px;font-size:0.88rem;font-family:inherit;outline:none}
.fg input:focus{border-color:var(--h)}
.iw{background:var(--hm);border-radius:8px;padding:12px 14px;font-size:0.82rem;line-height:1.6;border-left:3px solid var(--h)}
.iw strong{color:var(--ht);font-size:0.9rem}
.iw .tc{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px}
.ch2{background:#fff3cd;color:#7a5c00;padding:2px 9px;border-radius:8px;font-size:0.75rem;font-weight:600}
.ch2.tot{background:#fee2e2;color:#991b1b}
.mf{padding:13px 22px;background:#f5f5f5;border-top:1px solid var(--b);display:flex;gap:10px;justify-content:flex-end;flex-shrink:0}
.btl{background:#eee;border:none;padding:9px 18px;border-radius:8px;cursor:pointer;font-size:0.88rem;font-family:inherit}
.bcf{background:var(--h);color:#fff;border:none;padding:9px 20px;border-radius:8px;cursor:pointer;font-size:0.88rem;font-weight:700;font-family:inherit}
.bcf:hover{background:var(--ht)}
#print-area{display:none}
@media print{body>*{display:none!important}#print-area{display:block!important}@page{margin:2cm;size:A4 portrait}.sc{font-family:'Times New Roman',serif;font-size:12pt;line-height:1.6;page-break-after:always}.sc:last-child{page-break-after:avoid}.sc .kop{text-align:center;border-bottom:3px double black;padding-bottom:10px;margin-bottom:16px}.sc .kop-nama{font-size:14pt;font-weight:bold;text-transform:uppercase}.sc .kop-sub{font-size:11pt}.sc .judul{text-align:center;font-size:13pt;font-weight:bold;text-decoration:underline;text-transform:uppercase;margin:12px 0 4px}.sc .nomor{text-align:center;font-size:11pt;margin-bottom:18px}.sc .ti2{border-collapse:collapse}.sc .ti2 td{padding:2px 0;font-size:11pt;vertical-align:top}.sc .ti2 td:nth-child(2){padding:0 8px}.sc .para{margin-bottom:12pt;font-size:11pt;text-align:justify}.sc .nominal{text-align:center;font-size:13pt;font-weight:bold;margin:12pt 0 4pt}.sc .nominal-kecil{text-align:center;font-size:10pt;color:#333;margin-bottom:14pt}.sc .ttd2{display:flex;justify-content:flex-end;margin-top:24pt}.sc .ttd-box{text-align:center;min-width:210px}.sc .ttd-jabatan{font-weight:bold}.sc .ttd-spasi{height:70pt}.sc .ttd-nama{font-weight:bold;text-decoration:underline}}
@media(max-width:900px){.hbr{grid-template-columns:repeat(3,1fr)}.dg{grid-template-columns:repeat(3,1fr)}.cr{grid-template-columns:1fr}.mb{grid-template-columns:1fr}.mfc{border-right:none;border-bottom:1px solid var(--b);max-height:50vh}.mpc{max-height:50vh}}
@media(max-width:600px){.hbr{grid-template-columns:1fr 1fr}.dg{grid-template-columns:repeat(2,1fr)}.nbt h1{font-size:0.8rem}.nv{padding:8px 16px;font-size:0.75rem}}
</style>
</head>
<body>

<nav class="nb">
  <div class="nbi">
    <div class="nbl">🏛️</div>
    <div class="nbt">
      <h1>Dashboard PBB-P2 · Desa Kasomalang Kulon</h1>
      <p>Kecamatan Kasomalang, Kabupaten Subang · Tahun 2025</p>
    </div>
    <div class="nbb">BAPENDA 2025</div>
  </div>
  <div class="nt">
    <div class="nv aktif" id="tab-dashboard" onclick="showPage('dashboard')">
      📊 Dashboard <span>Analytics & Ringkasan</span>
    </div>
    <div class="nv" id="tab-data" onclick="showPage('data')">
      📋 Data Masyarakat <span>Daftar Tunggakan</span>
    </div>
  </div>
</nav>

<!-- PAGE 1: DASHBOARD -->
<div class="pg ak" id="page-dashboard">
  <div class="pd">
    <div class="hb">
      <div class="hl">💰 Total Tunggakan PBB-P2 · Desa Kasomalang Kulon</div>
      <div class="ha" id="hero-total">Rp 0</div>
      <div class="hs" id="hero-sub">Memuat...</div>
      <div class="hbr" id="hero-breakdown"></div>
    </div>

    <div class="st">📍 Ringkasan per Wilayah</div>
    <div class="dg" id="dusun-grid"></div>

    <div class="cr">
      <div class="cc">
        <div class="ct">📊 Total Tunggakan per RW</div>
        <div class="bc" id="chart-rw"></div>
      </div>
      <div class="cc">
        <div class="ct">📅 Total Tunggakan per Tahun</div>
        <div class="bc" id="chart-year"></div>
      </div>
    </div>

    <div class="st">🏅 10 Warga dengan Tunggakan Terbesar</div>
    <div class="td">
      <div class="tdh">
        <span>👑 Pemuka Tunggakan</span>
        <span id="top-count"></span>
      </div>
      <div class="tl" id="top-list"></div>
    </div>
  </div>
</div>

<!-- PAGE 2: DATA MASYARAKAT -->
<div class="pg" id="page-data">
  <div class="pdm">
    <div class="pc">
      <h2>🔍 Cari &amp; Filter Data Masyarakat</h2>
      <div class="fr">
        <input type="text" id="cari-nama" placeholder="Cari nama wajib pajak..." oninput="applyFilter()">
        <input type="text" id="cari-nop" placeholder="Cari Nomor SPPT / NOP..." oninput="applyFilter()">
        <select id="filter-dusun" onchange="onDusunSelect()">
          <option value="">Semua Wilayah</option>
          <option value="1">Dusun I (RW 01, 02)</option>
          <option value="2">Dusun II (RW 03, 06)</option>
          <option value="3">Dusun III (RW 04, 05, 07)</option>
          <option value="4">Luar (RW 0)</option>
        </select>
        <select id="filter-rw" onchange="onRwSelect()"><option value="">Semua RW</option></select>
        <select id="filter-rt" onchange="applyFilter()"><option value="">Semua RT</option></select>
        <select id="filter-tahun" onchange="applyFilter()">
          <option value="">Semua Tahun</option>
          <option value="2020">2020</option><option value="2021">2021</option>
          <option value="2022">2022</option><option value="2023">2023</option>
          <option value="2024">2024</option><option value="2025">2025</option>
        </select>
      </div>
      <div class="fab" id="filter-active-bar" style="display:none"></div>
    </div>

    <div class="pt">
      <div class="th">
        <span>Daftar Wajib Pajak Belum Bayar</span>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
          <span class="tt" id="info-terpilih">0 terpilih</span>
          <button class="bc2 hijau" onclick="cetakBatch('pemberitahuan')">📄 Pemberitahuan</button>
          <button class="bc2" onclick="cetakBatch('undangan')">✉️ Undangan</button>
        </div>
      </div>
      <div class="ts">
        <table>
          <thead>
            <tr>
              <th><input type="checkbox" id="pilih-semua" onchange="pilihSemua(this)"></th>
              <th>Nama Wajib Pajak</th><th>Nomor SPPT</th>
              <th>RT/RW</th><th>Wilayah</th><th>Tahun Tunggakan</th>
              <th>Total</th><th>Aksi</th>
            </tr>
          </thead>
          <tbody id="tbody-data"></tbody>
        </table>
      </div>
      <div id="empty-state" class="es" style="display:none">🔎 Tidak ada data yang sesuai</div>
      <div class="pg2" id="pagination"></div>
    </div>
  </div>
</div>

<!-- MODAL PEMBERITAHUAN -->
<div class="ov" id="modal-pb"><div class="md">
  <div class="mh"><h3>📄 Surat Pemberitahuan PBB-P2</h3><button onclick="tutupModal('pb')">×</button></div>
  <div class="mb">
    <div class="mfc">
      <div class="iw" id="iwb-pb"></div>
      <div class="fg"><label>Nomor Surat</label><input type="text" id="pb-nomor" value="001" oninput="rerender('pb')"></div>
      <div class="fg"><label>Alamat Wajib Pajak</label><input type="text" id="pb-alamat" placeholder="Kp. ..., RT .../RW ..." oninput="rerender('pb')"></div>
    </div>
    <div class="mpc">
      <div class="ptb">👁 Preview Surat</div>
      <div class="pb2"><div class="kp" id="prev-pb"></div></div>
    </div>
  </div>
  <div class="mf">
    <button class="btl" onclick="tutupModal('pb')">Batal</button>
    <button class="bcf" onclick="docetak('pb')">🖨️ Cetak Surat</button>
  </div>
</div></div>

<!-- MODAL UNDANGAN -->
<div class="ov" id="modal-und"><div class="md">
  <div class="mh und"><h3>✉️ Surat Undangan PBB-P2</h3><button onclick="tutupModal('und')">×</button></div>
  <div class="mb">
    <div class="mfc">
      <div class="iw" id="iwb-und"></div>
      <div class="fg"><label>Nomor Surat</label><input type="text" id="und-nomor" value="001" oninput="rerender('und')"></div>
      <div class="fg"><label>Alamat Wajib Pajak</label><input type="text" id="und-alamat" placeholder="Kp. ..." oninput="rerender('und')"></div>
      <div class="fg"><label>Hari / Tanggal</label><input type="text" id="und-hari" placeholder="Senin, 16 Juni 2025" oninput="rerender('und')"></div>
      <div class="fg"><label>Waktu</label><input type="text" id="und-waktu" value="09.00 WIB" oninput="rerender('und')"></div>
    </div>
    <div class="mpc">
      <div class="ptb">👁 Preview Surat</div>
      <div class="pb2"><div class="kp" id="prev-und"></div></div>
    </div>
  </div>
  <div class="mf">
    <button class="btl" onclick="tutupModal('und')">Batal</button>
    <button class="bcf" onclick="docetak('und')">🖨️ Cetak Surat</button>
  </div>
</div></div>

<div id="print-area"></div>

<script>
""")

new_html += "\n// ===== CONFIG =====\n"
new_html += dusun_s.strip() + "\n\n"
new_html += "// ===== DATA =====\n"
new_html += data_s.strip() + "\n\n"
new_html += "// ===== STATE =====\n"
new_html += state_s.strip() + "\n\n"

# add all functions
for n in fnames:
    if fns[n]:
        new_html += fns[n] + "\n\n"

# NEW: showPage function
new_html += """
// ===== PAGE NAVIGATION =====
function showPage(page) {
  document.querySelectorAll('.pg').forEach(p => p.classList.remove('ak'));
  document.querySelectorAll('.nv').forEach(t => t.classList.remove('aktif'));
  document.getElementById('page-' + page).classList.add('ak');
  document.getElementById('tab-' + page).classList.add('aktif');
  if (page === 'dashboard') {
    initDashboard();
  } else {
    applyFilter();
  }
}

// ===== DASHBOARD INIT =====
function initDashboard() {
  const total = PBB_DATA.reduce((s,d) => s + d.total, 0);
  const totalWp = PBB_DATA.length;
  animateCounter(document.getElementById('hero-total'), total, true, 1800);
  document.getElementById('hero-sub').textContent = totalWp + ' Wajib Pajak · 3 Daven · Semua Tahun';

  // Hero breakdown - 5 stats
  const dStats = [];
  for (let d = 0; d <= 4; d++) {
    let subset;
    if (d === 0) subset = PBB_DATA;
    else if (d === 4) subset = PBB_DATA.filter(x => x.rw === '0');
    else subset = PBB_DATA.filter(x => getDusun(x.rw) === d);
    dStats.push({ count: subset.length, total: subset.reduce((s,x) => s+x.total,0) });
  }
  const labels = ['Semua','Dusun I','Dusun II','Dusun III','Luar'];
  document.getElementById('hero-breakdown').innerHTML = dStats.map((ds,i) =>
    '<div class="hbs">' +
      '<div class="hbsn">' + rp(ds.total) + '</div>' +
      '<div class="hbsl">' + labels[i] + '</div>' +
      '<div class="hbsl">' + ds.count + ' WP</div>' +
    '</div>'
  ).join('');

  // Daven cards
  const cardLabels = ['🏘️ Semua','🌿 Daven I','🌿 Daven II','🌿 Daven III','🌐 Luar'];
  const cardRws   = ['RW 1–7','RW 01 · RW 02','RW 03 · RW 06','RW 04 · RW 05 · RW 07','RW 0'];
  const maxTotal = Math.max(...dStats.map(ds=>ds.total));

  let cardsHtml = '';
  for (let d = 0; d <= 4; d++) {
    const ds = dStats[d];
    const pct = (ds.total / maxTotal * 100).toFixed(1);
    const extra = d === 4 ? ' lu' : '';
    cardsHtml +=
      '<div class="dc' + extra + '" id="dcard-d' + d + '" onclick="gotoData(d)">' +
        '<div class="di">' + cardLabels[d] + '</div>' +
        '<div class="dn">' + cardLabels[d].split(' ')[1] + '</div>' +
        '<div class="dr">' + cardRws[d] + '</div>' +
        '<div class="dc2">' + ds.count + ' WP</div>' +
        '<div class="dt">' + rp(ds.total) + '</div>' +
        '<div class="dbr"><div class="dbf" id="dbar-d' + d + '" style="width:0%"></div></div>' +
      '</div>';
  }
  document.getElementById('dusun-grid').innerHTML = cardsHtml;

  // Animate bars after a frame
  setTimeout(() => {
    for (let d = 0; d <= 4; d++) {
      const pct = (dStats[d].total / maxTotal * 100).toFixed(1);
      const bar = document.getElementById('dbar-d' + d);
      if (bar) bar.style.width = pct + '%';
    }
  }, 100);

  // RW Chart
  const rwMap = {};
  PBB_DATA.forEach(d => {
    const r = d.rw || '0';
    if (!rwMap[r]) rwMap[r] = 0;
    rwMap[r] += d.total;
  });
  const rwLabels = Object.keys(rwMap).sort((a,b) => +a - +b);
  const maxRw = Math.max(...Object.values(rwMap));
  const rwColors = ['h','e','m','u','a2','h','e','m','u','a2'];
  document.getElementById('chart-rw').innerHTML = rwLabels.map((r,i) => {
    const v = rwMap[r];
    const w = maxRw > 0 ? (v / maxRw * 100).toFixed(1) : 0;
    const c = rwColors[i % rwColors.length];
    return '<div class="br">' +
      '<div class="bl">RW ' + r + '</div>' +
      '<div class="bt"><div class="bf ' + c + '" style="width:' + w + '%">' + rp(v) + '</div></div>' +
      '<div class="bv">' + rp(v) + '</div>' +
    '</div>';
  }).join('');

  // Year Chart
  const yearMap = {};
  PBB_DATA.forEach(d => {
    Object.entries(d.tunggakan).forEach(([t, v]) => {
      if (!yearMap[t]) yearMap[t] = 0;
      yearMap[t] += v;
    });
  });
  const yearLabels = ['2020','2021','2022','2023','2024','2025'];
  const yearVals   = yearLabels.map(y => yearMap[y] || 0);
  const maxYear    = Math.max(...yearVals, 1);
  document.getElementById('chart-year').innerHTML = yearLabels.map((y,i) => {
    const v = yearVals[i];
    const w = (v / maxYear * 100).toFixed(1);
    const c = rwColors[i % rwColors.length];
    return '<div class="br">' +
      '<div class="bl">' + y + '</div>' +
      '<div class="bt"><div class="bf ' + c + '" style="width:' + w + '%">' + rp(v) + '</div></div>' +
      '<div class="bv">' + rp(v) + '</div>' +
    '</div>';
  }).join('');

  // Top 10 debtors
  const sorted = [...PBB_DATA].sort((a,b) => b.total - a.total).slice(0, 10);
  const ranks = ['gold','silver','bronze','normal','normal','normal','normal','normal','normal','normal'];
  document.getElementById('top-count').textContent = 'Total 10 besar: ' + rp(sorted.reduce((s,d)=>s+d.total,0));
  document.getElementById('top-list').innerHTML = sorted.map((d,i) =>
    '<div class="ti">' +
      '<div class="tr2 ' + ranks[i] + '">' + (i+1) + '</div>' +
      '<div class="ti2">' +
        '<div class="tn">' + d.nama + '</div>' +
        '<div class="tm">RT ' + d.rt + '/RW ' + d.rw + ' · ' + getDusunLabel(d.rw) + '</div>' +
      '</div>' +
      '<div class="ta">' + rp(d.total) + '</div>' +
    '</div>'
  ).join('');
}

// Navigate to data page filtered by dusun
function gotoData(d) {
  if (d === 0) {
    document.getElementById('filter-dusun').value = '';
  } else {
    document.getElementById('filter-dusun').value = String(d);
  }
  showPage('data');
  onDusunSelect();
}

// Override init - called on DOMContentLoaded
const _origInit = typeof init !== 'undefined' ? init : function() {};
window.addEventListener('DOMContentLoaded', function() {
  initDashboard();
  applyFilter();
});
"""

new_html += "\n</script>\n</body>\n</html>\n"

print(f"Generated: {len(new_html)} chars")

with open(out, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Saved to: {out}")