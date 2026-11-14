import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="California Trip Planner & Checklist",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove default Streamlit padding and header so the planner fills the screen cleanly
st.markdown(
    """
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header[data-testid="stHeader"] { display: none; }
        footer { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>California Trip Planner & Checklist — Omar</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
          },
          colors: {
            navy: {
              950: '#08111e',
              900: '#0f1e36',
              800: '#172c4d',
              700: '#213c66',
            },
            sunset: {
              400: '#fbbf24',
              500: '#f59e0b',
              600: '#d97706',
            },
            lagoon: {
              400: '#2dd4bf',
              500: '#14b8a6',
              600: '#0d9488',
            }
          }
        }
      }
    };
  </script>
  <style>
    .custom-checkbox {
      appearance: none;
      -webkit-appearance: none;
      width: 1.35rem;
      height: 1.35rem;
      border-radius: 0.45rem;
      border: 2px solid #cbd5e1;
      background-color: #ffffff;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
      flex-shrink: 0;
    }
    .custom-checkbox:hover {
      border-color: #0d9488;
      transform: scale(1.06);
    }
    .custom-checkbox:checked {
      background-color: #0d9488;
      border-color: #0d9488;
      transform: scale(1.04);
    }
    .custom-checkbox:checked::after {
      content: '';
      width: 0.38rem;
      height: 0.7rem;
      border: solid white;
      border-width: 0 2.5px 2.5px 0;
      transform: rotate(45deg) translate(-0.5px, -0.5px);
    }
    .item-label {
      transition: color 0.2s ease, opacity 0.2s ease;
    }
    .item-checked .item-label {
      text-decoration: line-through;
      color: #94a3b8;
    }
    .item-checked .item-subtext {
      opacity: 0.6;
    }
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    @media print {
      body {
        background: #ffffff !important;
        color: #0f172a !important;
      }
      .no-print {
        display: none !important;
      }
      .print-only {
        display: block !important;
      }
      .print-card {
        box-shadow: none !important;
        border: 1px solid #cbd5e1 !important;
        break-inside: avoid;
      }
      header {
        background: #0f1e36 !important;
        color: #ffffff !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
    }
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- Toast Notification Container -->
  <div id="toast-container" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none"></div>

  <!-- Top Header Dashboard -->
  <header class="bg-gradient-to-br from-navy-950 via-navy-900 to-navy-800 text-white shadow-xl border-b border-navy-700/60">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">
        <div>
          <div class="flex flex-wrap items-center gap-2.5 mb-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-sunset-500/20 text-sunset-400 border border-sunset-400/30">
              <span>☀️</span> Los Angeles, CA • Sister's Wedding
            </span>
            <span id="countdown-badge" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-lagoon-500/20 text-lagoon-400 border border-lagoon-400/30">
              ⏳ Calculating countdown...
            </span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            California Trip Planner &amp; Checklist
          </h1>
          <p class="text-slate-300 text-sm sm:text-base mt-1 flex flex-wrap items-center gap-x-3 gap-y-1">
            <span class="font-medium text-white">📅 Fri, Nov 20 – Sun, Nov 22, 2026</span>
            <span class="text-slate-500 hidden sm:inline">•</span>
            <span class="text-slate-300">✈️ JFK → LAX (Nov 19 Night Departure)</span>
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-2.5 no-print">
          <button onclick="openItemModal()" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-sunset-500 hover:bg-sunset-600 text-navy-950 font-bold text-sm shadow-lg shadow-sunset-500/20 transition active:scale-95 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
            Add Item
          </button>
          <button onclick="openBackupModal()" class="inline-flex items-center gap-2 px-3.5 py-2.5 rounded-xl bg-lagoon-500/20 hover:bg-lagoon-500/30 text-lagoon-300 font-semibold text-sm border border-lagoon-400/30 transition active:scale-95 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"/></svg>
            Save / Load
          </button>
          <button onclick="openExportModal()" class="inline-flex items-center gap-2 px-3.5 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-medium text-sm border border-white/15 transition active:scale-95 cursor-pointer">
            <svg class="w-4 h-4 text-lagoon-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
            Export / Print
          </button>
          <button onclick="confirmAction('reset')" class="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-white/5 hover:bg-rose-500/20 text-slate-300 hover:text-rose-200 font-medium text-sm border border-white/10 hover:border-rose-400/30 transition active:scale-95 cursor-pointer" title="Uncheck all items">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            Reset All
          </button>
        </div>
      </div>

      <div class="mt-6 bg-navy-950/60 border border-white/10 rounded-2xl p-4 sm:p-5">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-2.5">
          <span class="text-xs sm:text-sm font-semibold uppercase tracking-wider text-slate-300">Overall Packing &amp; Prep Progress</span>
          <span id="overall-progress-text" class="text-sm sm:text-base font-bold text-lagoon-400">0 / 35 Packed &amp; Ready (0%)</span>
        </div>
        <div class="w-full h-3.5 bg-navy-800 rounded-full overflow-hidden p-0.5 border border-white/5">
          <div id="overall-progress-bar" class="h-full rounded-full bg-gradient-to-r from-sunset-500 via-amber-400 to-lagoon-400 transition-all duration-500 ease-out" style="width: 0%"></div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="max-w-6xl mx-auto w-full px-4 sm:px-6 py-6 sm:py-8 flex-1 space-y-6">

    <!-- Collapsible Trip Logistics Summary Section -->
    <section class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden print-card">
      <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200/80 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-lg">🗂️</span>
          <h2 class="font-bold text-slate-800 text-sm sm:text-base">Trip Logistics &amp; Priority Reminders</h2>
        </div>
        <button id="toggle-logistics-btn" onclick="toggleLogistics()" class="no-print text-xs font-semibold text-lagoon-600 hover:text-lagoon-700 flex items-center gap-1 px-2.5 py-1 rounded-lg hover:bg-lagoon-50 transition cursor-pointer">
          <span id="toggle-logistics-label">Hide Details</span>
          <svg id="toggle-logistics-icon" class="w-4 h-4 transition-transform duration-200" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/></svg>
        </button>
      </div>

      <div id="logistics-body" class="p-5 grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div class="lg:col-span-7 rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-4 sm:p-5 flex flex-col justify-between relative">
          <div>
            <div class="flex flex-wrap items-start justify-between gap-2 mb-3">
              <div class="flex items-center gap-2.5">
                <div class="w-10 h-10 rounded-xl bg-navy-900 text-sunset-400 flex items-center justify-center text-lg font-bold shadow-sm">
                  🚙
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <h3 class="font-bold text-slate-900 text-base">Budget Rent A Car</h3>
                    <span class="px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide rounded-md bg-emerald-100 text-emerald-800">Confirmed</span>
                  </div>
                  <p class="text-xs font-medium text-slate-500">Lincoln Navigator (or similar) • Full-Size Luxury SUV</p>
                </div>
              </div>

              <button onclick="copyText('07264298US6', 'Rental Car Conf #07264298US6 copied!')" class="no-print inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-navy-900 hover:bg-navy-800 text-white text-xs font-semibold shadow-sm transition active:scale-95 cursor-pointer">
                <span class="text-sunset-400 font-mono">#07264298US6</span>
                <svg class="w-3.5 h-3.5 text-slate-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                <span>Copy Conf #</span>
              </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 my-3 text-xs">
              <div class="p-3 rounded-xl bg-white border border-slate-200/80">
                <span class="text-[11px] font-bold uppercase tracking-wider text-lagoon-600 block mb-0.5">Pickup</span>
                <p class="font-bold text-slate-800">Fri, Nov 20, 2026 • 1:30 AM</p>
                <p class="text-slate-500 mt-0.5">LAX Consolidated Rent-A-Car (ConRAC)</p>
              </div>
              <div class="p-3 rounded-xl bg-white border border-slate-200/80">
                <span class="text-[11px] font-bold uppercase tracking-wider text-sunset-600 block mb-0.5">Dropoff &amp; Total</span>
                <p class="font-bold text-slate-800">Sun, Nov 22, 2026 • 3:00 PM</p>
                <p class="text-slate-600 font-semibold mt-0.5">Est. Total: <span class="text-slate-900">$464.33</span></p>
              </div>
            </div>

            <div class="text-xs text-slate-600 space-y-1.5 mt-2">
              <p class="flex items-start gap-1.5">
                <span class="text-slate-400 mt-0.5">📍</span>
                <span><strong class="text-slate-700">Address:</strong> 5251 W 98th St, Los Angeles, CA 90045</span>
              </p>
              <div class="p-2.5 rounded-xl bg-purple-50 border border-purple-200/80 text-purple-900 flex items-start gap-2">
                <span class="text-sm leading-none mt-0.5">🚌</span>
                <span><strong>Shuttle Tip:</strong> Follow Purple <em>"Rental Car Shuttles"</em> signs on Lower/Arrivals outer island curb.</span>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-5 rounded-2xl border border-slate-200 bg-gradient-to-br from-amber-50/50 via-white to-white p-4 sm:p-5 flex flex-col justify-between space-y-4">
          <div>
            <div class="flex items-center justify-between gap-2 mb-3">
              <div class="flex items-center gap-2.5">
                <div class="w-10 h-10 rounded-xl bg-sunset-500/15 text-sunset-600 flex items-center justify-center text-lg font-bold">
                  🏨
                </div>
                <div>
                  <h3 class="font-bold text-slate-900 text-base">Hotel &amp; Wedding Tasks</h3>
                  <p class="text-xs text-slate-500">Key pre-departure action items</p>
                </div>
              </div>
              <button onclick="openItemModal('Travel, Bookings & Wedding')" class="no-print inline-flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-sunset-500 hover:bg-sunset-600 text-navy-950 text-xs font-bold shadow-2xs transition active:scale-95 cursor-pointer" title="Add task to Hotel & Wedding Tasks">
                <span>+ Add Task</span>
              </button>
            </div>

            <div id="hotel-wedding-tasks-list" class="space-y-2.5 max-h-64 overflow-y-auto pr-0.5"></div>
          </div>

          <div class="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-[11px] text-slate-500">
            <span>✈️ Out: <strong>Delta 0752</strong> (<button onclick="copyText('GUT49I', 'Delta Conf #GUT49I copied!')" class="underline hover:text-navy-900 font-mono cursor-pointer">GUT49I</button>)</span>
            <span>✈️ Ret: <strong>JetBlue 0524</strong> (<button onclick="copyText('QYYWWI', 'JetBlue Conf #QYYWWI copied!')" class="underline hover:text-navy-900 font-mono cursor-pointer">QYYWWI</button>)</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Controls: Search, Hide Completed Toggle & Category Tabs -->
    <section class="space-y-3 no-print">
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        <div class="relative flex-1 max-w-md">
          <svg class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input id="search-input" type="text" placeholder="Search packing items, notes, or confirmation #..." oninput="renderChecklist()" class="w-full pl-10 pr-8 py-2.5 rounded-xl bg-white border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-lagoon-500 focus:border-transparent shadow-sm" />
          <button id="clear-search-btn" onclick="clearSearch()" class="hidden absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 text-xs font-bold px-1.5 py-0.5 rounded cursor-pointer">✕</button>
        </div>

        <div class="flex flex-wrap items-center gap-2.5">
          <label class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-700 cursor-pointer shadow-sm hover:bg-slate-50 select-none">
            <input id="hide-completed-toggle" type="checkbox" onchange="toggleHideCompleted()" class="rounded text-lagoon-600 focus:ring-lagoon-500 w-4 h-4 cursor-pointer" />
            <span>Hide Completed</span>
          </label>

          <button onclick="confirmAction('restore')" class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-50 shadow-sm transition cursor-pointer" title="Revert all items back to the original 35-item trip list">
            <span>↺ Restore Default List</span>
          </button>
        </div>
      </div>

      <div id="category-tabs" class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1"></div>
    </section>

    <!-- Dynamic Checklist Container -->
    <section id="checklist-container" class="space-y-6"></section>

  </main>

  <!-- Footer -->
  <footer class="max-w-6xl mx-auto w-full px-4 sm:px-6 py-6 text-center text-xs text-slate-400 border-t border-slate-200/70 mt-8 no-print">
    <p id="storage-status-text">Checking storage availability... • California Trip Planner (Nov 20–22, 2026)</p>
  </footer>

  <!-- Modal: Save / Load Progress Backup -->
  <div id="backup-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-navy-950/60 backdrop-blur-xs p-4">
    <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-lg overflow-hidden">
      <div class="px-5 py-4 bg-navy-900 text-white flex items-center justify-between">
        <h3 class="font-bold text-base">Save &amp; Restore Progress</h3>
        <button onclick="closeBackupModal()" class="text-slate-300 hover:text-white text-lg font-bold leading-none cursor-pointer">✕</button>
      </div>
      <div class="p-5 space-y-4">
        <div id="sandbox-warning-banner" class="hidden p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 leading-relaxed">
          <strong>Tip for Streamlit / Preview Windows:</strong> Embedded frames may clear browser storage on reload. Use <strong>Download Backup</strong> or <strong>Copy Save Code</strong> below to keep your progress permanently.
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          <button onclick="downloadBackupFile()" class="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-navy-900 hover:bg-navy-800 text-white text-xs font-bold shadow-sm transition cursor-pointer">
            <span>⬇️ Download Backup (.json)</span>
          </button>
          <label class="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-lagoon-600 hover:bg-lagoon-700 text-white text-xs font-bold shadow-sm transition cursor-pointer">
            <span>⬆️ Load Backup (.json)</span>
            <input type="file" accept=".json,application/json" onchange="uploadBackupFile(event)" class="hidden" />
          </label>
        </div>

        <div class="pt-2 border-t border-slate-100 space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-xs font-bold uppercase tracking-wider text-slate-600">Save Code (Copy or Paste to Restore)</label>
            <button onclick="copySaveCode()" class="text-xs font-bold text-lagoon-600 hover:text-lagoon-700 cursor-pointer">📋 Copy Code</button>
          </div>
          <textarea id="save-code-textarea" rows="4" placeholder="Paste a previously copied save code here..." class="w-full p-3 rounded-xl bg-slate-50 border border-slate-200 font-mono text-[11px] text-slate-700 focus:outline-none focus:ring-2 focus:ring-lagoon-500"></textarea>
          <div class="flex justify-end">
            <button onclick="restoreFromSaveCode()" class="px-4 py-2 rounded-xl bg-sunset-500 hover:bg-sunset-600 text-navy-950 text-xs font-bold cursor-pointer">
              Restore From Pasted Code
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: Add / Edit Checklist Item -->
  <div id="item-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-navy-950/60 backdrop-blur-xs p-4">
    <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-md overflow-hidden transform transition-all">
      <div class="px-5 py-4 bg-navy-900 text-white flex items-center justify-between">
        <h3 id="modal-title" class="font-bold text-base">Add New Checklist Item</h3>
        <button onclick="closeItemModal()" class="text-slate-300 hover:text-white text-lg font-bold leading-none cursor-pointer">✕</button>
      </div>
      <form id="item-form" onsubmit="saveItemForm(event)" class="p-5 space-y-4">
        <input type="hidden" id="edit-item-id" value="" />
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">Category</label>
          <select id="item-category-input" required class="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-lagoon-500">
            <option value="Travel, Bookings & Wedding">Travel, Bookings &amp; Wedding</option>
            <option value="Omar's Packing">Omar's Packing</option>
            <option value="Kids' Packing (Per Child)">Kids' Packing (Per Child)</option>
            <option value="Outerwear, Gear & Toiletries">Outerwear, Gear &amp; Toiletries</option>
            <option value="Snacks & Drinks">Snacks &amp; Drinks</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">Item Name *</label>
          <input id="item-label-input" type="text" required placeholder="e.g., Dress shirt, Stroller, Car seats..." class="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-lagoon-500" />
        </div>
        <div>
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-1.5">Sub-note / Details (Optional)</label>
          <textarea id="item-subtext-input" rows="2" placeholder="e.g., Confirmation #, quantity, or packing reminder..." class="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-lagoon-500"></textarea>
        </div>
        <div class="pt-2 flex items-center justify-end gap-2.5">
          <button type="button" onclick="closeItemModal()" class="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 text-sm font-semibold cursor-pointer">Cancel</button>
          <button type="submit" class="px-5 py-2 rounded-xl bg-lagoon-600 hover:bg-lagoon-700 text-white text-sm font-bold shadow-sm cursor-pointer">Save Item</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal: Export / Print Preview -->
  <div id="export-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-navy-950/60 backdrop-blur-xs p-4">
    <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]">
      <div class="px-5 py-4 bg-navy-900 text-white flex items-center justify-between">
        <h3 class="font-bold text-base">Export or Print California Trip Checklist</h3>
        <button onclick="closeExportModal()" class="text-slate-300 hover:text-white text-lg font-bold leading-none cursor-pointer">✕</button>
      </div>
      <div class="p-5 overflow-y-auto flex-1 space-y-3">
        <p class="text-xs text-slate-500">Copy this formatted checklist to paste into Notes, WhatsApp, or email—or print a clean paper checklist.</p>
        <textarea id="export-textarea" readonly rows="14" class="w-full p-3.5 rounded-xl bg-slate-50 border border-slate-200 font-mono text-xs text-slate-800 focus:outline-none"></textarea>
      </div>
      <div class="px-5 py-3.5 bg-slate-50 border-t border-slate-200 flex flex-wrap items-center justify-end gap-2.5">
        <button onclick="closeExportModal()" class="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-white text-sm font-semibold cursor-pointer">Close</button>
        <button onclick="copyExportText()" class="px-4 py-2 rounded-xl bg-navy-900 hover:bg-navy-800 text-white text-sm font-bold cursor-pointer">📋 Copy Checklist Text</button>
        <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-sunset-500 hover:bg-sunset-600 text-navy-950 text-sm font-bold cursor-pointer">🖨️ Print Page</button>
      </div>
    </div>
  </div>

  <!-- Modal: Custom Confirmation Dialog -->
  <div id="confirm-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-navy-950/60 backdrop-blur-xs p-4">
    <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-sm overflow-hidden">
      <div class="p-5">
        <h3 id="confirm-title" class="font-bold text-slate-900 text-base">Are you sure?</h3>
        <p id="confirm-message" class="text-sm text-slate-600 mt-1.5"></p>
        <div class="mt-5 flex items-center justify-end gap-2.5">
          <button onclick="closeConfirmModal()" class="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 text-sm font-semibold cursor-pointer">Cancel</button>
          <button id="confirm-proceed-btn" class="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-sm font-bold cursor-pointer">Confirm</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    const STORAGE_KEY = 'omar_california_trip_planner_v1';

    const CATEGORIES = [
      { id: "Travel, Bookings & Wedding", icon: "✈️", color: "sky" },
      { id: "Omar's Packing", icon: "🧳", color: "indigo" },
      { id: "Kids' Packing (Per Child)", icon: "👶", color: "amber" },
      { id: "Outerwear, Gear & Toiletries", icon: "🧥", color: "teal" },
      { id: "Snacks & Drinks", icon: "🍎", color: "rose" }
    ];

    const KIDS_NAMES = ["Adham", "Sulaiman", "Yasin", "Saif-Eddine"];

    const DEFAULT_ITEMS = [
      { id: "item-1", category: "Travel, Bookings & Wedding", label: "Hotel booking", subtext: "", checked: false },
      {
        id: "item-2",
        category: "Travel, Bookings & Wedding",
        label: "Car booking",
        subtext: "Budget Rent A Car • Conf #07264298US6 • Lincoln Navigator or similar | Pickup: Fri, Nov 20, 2026 at 1:30 AM • Dropoff: Sun, Nov 22 at 3:00 PM (LAX - 5251 W 98th St) | Total: $464.33",
        checked: true
      },
      { id: "item-3", category: "Travel, Bookings & Wedding", label: "Wedding gift", subtext: "Pull $1,000 cash from bank", checked: false },

      { id: "item-4", category: "Omar's Packing", label: "Suit", subtext: "", checked: false },
      { id: "item-5", category: "Omar's Packing", label: "Tie", subtext: "", checked: false },
      { id: "item-6", category: "Omar's Packing", label: "Brown shoes", subtext: "", checked: false },
      { id: "item-7", category: "Omar's Packing", label: "Casual shoes", subtext: "", checked: false },
      { id: "item-8", category: "Omar's Packing", label: "Dress socks", subtext: "", checked: false },
      { id: "item-9", category: "Omar's Packing", label: "Regular socks", subtext: "", checked: false },
      { id: "item-10", category: "Omar's Packing", label: "2 casual outfits", subtext: "", checked: false },
      { id: "item-11", category: "Omar's Packing", label: "Pajamas", subtext: "", checked: false },
      { id: "item-12", category: "Omar's Packing", label: "Underwear", subtext: "", checked: false },
      { id: "item-13", category: "Omar's Packing", label: "Backpack", subtext: "", checked: false },
      { id: "item-14", category: "Omar's Packing", label: "Xbox", subtext: "", checked: false },
      { id: "item-15", category: "Omar's Packing", label: "Cologne", subtext: "", checked: false },
      { id: "item-16", category: "Omar's Packing", label: "Toothbrush", subtext: "", checked: false },

      { id: "item-17", category: "Kids' Packing (Per Child)", label: "Suit", subtext: "", checked: false },
      { id: "item-18", category: "Kids' Packing (Per Child)", label: "Suit shirts", subtext: "", checked: false },
      { id: "item-19", category: "Kids' Packing (Per Child)", label: "Belts", subtext: "", checked: false },
      { id: "item-20", category: "Kids' Packing (Per Child)", label: "2 casual outfits", subtext: "", checked: false },
      { id: "item-21", category: "Kids' Packing (Per Child)", label: "1 play outfit", subtext: "", checked: false },
      { id: "item-22", category: "Kids' Packing (Per Child)", label: "Pajamas (PJs)", subtext: "", checked: false },
      { id: "item-23", category: "Kids' Packing (Per Child)", label: "Underwear", subtext: "", checked: false },
      { id: "item-24", category: "Kids' Packing (Per Child)", label: "Pull-ups", subtext: "", checked: false },
      { id: "item-25", category: "Kids' Packing (Per Child)", label: "Socks", subtext: "", checked: false },
      { id: "item-26", category: "Kids' Packing (Per Child)", label: "1 pair of regular shoes", subtext: "", checked: false },
      { id: "item-27", category: "Kids' Packing (Per Child)", label: "1 pair of casual shoes", subtext: "", checked: false },
      { id: "item-28", category: "Kids' Packing (Per Child)", label: "1 pair of suit shoes", subtext: "", checked: false },

      { id: "item-29", category: "Outerwear, Gear & Toiletries", label: "Jackets", subtext: "", checked: false },
      { id: "item-30", category: "Outerwear, Gear & Toiletries", label: "Travel steamer", subtext: "", checked: false },
      { id: "item-31", category: "Outerwear, Gear & Toiletries", label: "Kids' toothpaste", subtext: "", checked: false },
      { id: "item-32", category: "Outerwear, Gear & Toiletries", label: "iPads", subtext: "", checked: false },
      { id: "item-33", category: "Outerwear, Gear & Toiletries", label: "Kids' headphones", subtext: "", checked: false },
      { id: "item-34", category: "Outerwear, Gear & Toiletries", label: "Chargers", subtext: "", checked: false },

      { id: "item-35", category: "Snacks & Drinks", label: "Juice and snacks", subtext: "", checked: false }
    ];

    let state = {
      items: [],
      activeCategory: 'ALL',
      hideCompleted: false,
      logisticsCollapsed: false,
      kidMode: 'MASTER',
      kidProgress: {}
    };

    let isLocalStorageAvailable = false;

    function detectStorage() {
      try {
        const testKey = '__storage_test__';
        localStorage.setItem(testKey, '1');
        localStorage.removeItem(testKey);
        return true;
      } catch (e) {
        return false;
      }
    }

    function encodeStateToHash(dataObj) {
      try {
        const json = JSON.stringify(dataObj);
        return btoa(unescape(encodeURIComponent(json)));
      } catch (e) {
        return '';
      }
    }

    function decodeStateFromHash(str) {
      try {
        const json = decodeURIComponent(escape(atob(str)));
        return JSON.parse(json);
      } catch (e) {
        return null;
      }
    }

    function applyParsedState(parsed) {
      if (!parsed || typeof parsed !== 'object') return false;
      state.items = Array.isArray(parsed.items) && parsed.items.length ? parsed.items : JSON.parse(JSON.stringify(DEFAULT_ITEMS));
      state.activeCategory = parsed.activeCategory || 'ALL';
      state.hideCompleted = Boolean(parsed.hideCompleted);
      state.logisticsCollapsed = Boolean(parsed.logisticsCollapsed);
      state.kidMode = parsed.kidMode || 'MASTER';
      state.kidProgress = parsed.kidProgress || {};
      ensureKidProgressStructure();
      return true;
    }

    function loadState() {
      isLocalStorageAvailable = detectStorage();
      let loaded = false;

      if (window.location.hash && window.location.hash.startsWith('#state=')) {
        const encoded = window.location.hash.slice(7);
        const fromHash = decodeStateFromHash(encoded);
        if (applyParsedState(fromHash)) {
          loaded = true;
        }
      }

      if (!loaded && isLocalStorageAvailable) {
        try {
          const saved = localStorage.getItem(STORAGE_KEY);
          if (saved) {
            const parsed = JSON.parse(saved);
            if (applyParsedState(parsed)) {
              loaded = true;
            }
          }
        } catch (err) {
          console.error('Error loading localStorage state:', err);
        }
      }

      if (!loaded) {
        state.items = JSON.parse(JSON.stringify(DEFAULT_ITEMS));
        ensureKidProgressStructure();
      }

      updateStorageStatusUI();
    }

    function saveState() {
      const encoded = encodeStateToHash(state);
      if (encoded) {
        try {
          history.replaceState(null, '', '#state=' + encoded);
        } catch (e) {}
      }

      if (isLocalStorageAvailable) {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        } catch (err) {
          console.error('Error saving state to localStorage:', err);
        }
      }
    }

    function updateStorageStatusUI() {
      const footerEl = document.getElementById('storage-status-text');
      const warningBanner = document.getElementById('sandbox-warning-banner');
      const isInIframe = window.self !== window.top;
      if (!isLocalStorageAvailable || isInIframe) {
        if (footerEl) {
          footerEl.innerHTML = '⚠️ Embedded frame detected: Use <strong>Save / Load</strong> in the top bar to keep changes permanently • California Trip Planner';
        }
        if (warningBanner) {
          warningBanner.classList.remove('hidden');
        }
      } else if (footerEl) {
        footerEl.textContent = 'Auto-saved locally in your browser • California Trip Planner (Nov 20–22, 2026)';
      }
    }

    function openBackupModal() {
      document.getElementById('save-code-textarea').value = encodeStateToHash(state);
      const modal = document.getElementById('backup-modal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeBackupModal() {
      const modal = document.getElementById('backup-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function downloadBackupFile() {
      const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'california-trip-checklist-backup.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('Backup file downloaded!');
    }

    function uploadBackupFile(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const parsed = JSON.parse(e.target.result);
          if (applyParsedState(parsed)) {
            saveState();
            document.getElementById('hide-completed-toggle').checked = state.hideCompleted;
            applyLogisticsCollapseUI();
            renderChecklist();
            closeBackupModal();
            showToast('Checklist restored from backup file!');
          } else {
            showToast('Invalid backup file format.');
          }
        } catch (err) {
          showToast('Could not read backup file.');
        }
      };
      reader.readAsText(file);
      event.target.value = '';
    }

    function copySaveCode() {
      const textarea = document.getElementById('save-code-textarea');
      textarea.select();
      try {
        document.execCommand('copy');
        showToast('Save code copied to clipboard!');
      } catch (e) {
        showToast('Select and copy the code manually.');
      }
    }

    function restoreFromSaveCode() {
      const raw = document.getElementById('save-code-textarea').value.trim();
      const cleaned = raw.startsWith('#state=') ? raw.slice(7) : raw;
      const parsed = decodeStateFromHash(cleaned);
      if (applyParsedState(parsed)) {
        saveState();
        document.getElementById('hide-completed-toggle').checked = state.hideCompleted;
        applyLogisticsCollapseUI();
        renderChecklist();
        closeBackupModal();
        showToast('Progress restored from save code!');
      } else {
        showToast('Invalid save code—please check and try again.');
      }
    }

    function ensureKidProgressStructure() {
      state.items.forEach(item => {
        if (item.category === "Kids' Packing (Per Child)") {
          if (!state.kidProgress[item.id]) {
            state.kidProgress[item.id] = {};
          }
          KIDS_NAMES.forEach(kid => {
            if (typeof state.kidProgress[item.id][kid] !== 'boolean') {
              state.kidProgress[item.id][kid] = item.checked;
            }
          });
        }
      });
    }

    function updateCountdown() {
      const badge = document.getElementById('countdown-badge');
      const tripStart = new Date('2026-11-20T00:00:00');
      const tripEnd = new Date('2026-11-22T23:59:59');
      const now = new Date();

      const todayMidnight = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      const startMidnight = new Date(tripStart.getFullYear(), tripStart.getMonth(), tripStart.getDate());
      const diffDays = Math.round((startMidnight - todayMidnight) / (1000 * 60 * 60 * 24));

      if (diffDays > 1) {
        badge.innerHTML = `⏳ ${diffDays} Days Until Trip`;
      } else if (diffDays === 1) {
        badge.innerHTML = `🔥 Tomorrow! (Flight Thu Night)`;
      } else if (diffDays === 0) {
        badge.innerHTML = `🎉 Trip Starts Today!`;
      } else if (now <= tripEnd) {
        badge.innerHTML = `🌴 Currently in California!`;
      } else {
        badge.innerHTML = `✅ Trip Completed`;
      }
    }

    function updateProgressUI() {
      const total = state.items.length;
      const completed = state.items.filter(i => i.checked).length;
      const pct = total === 0 ? 0 : Math.round((completed / total) * 100);

      document.getElementById('overall-progress-text').textContent = `${completed} / ${total} Packed & Ready (${pct}%)`;
      document.getElementById('overall-progress-bar').style.width = `${pct}%`;

      const tasksContainer = document.getElementById('hotel-wedding-tasks-list');
      if (tasksContainer) {
        const hotelWeddingTasks = state.items.filter(
          i => i.category === 'Travel, Bookings & Wedding' && i.id !== 'item-2'
        );

        if (hotelWeddingTasks.length === 0) {
          tasksContainer.innerHTML = `
            <div class="p-3.5 rounded-xl bg-white border border-dashed border-slate-300 text-center">
              <p class="text-xs text-slate-500">No tasks yet. Click <strong>+ Add Task</strong> above to add hotel or wedding action items.</p>
            </div>
          `;
        } else {
          tasksContainer.innerHTML = hotelWeddingTasks.map(task => {
            const isGift = task.id === 'item-3' || task.label.toLowerCase().includes('wedding gift');
            const isHotel = task.id === 'item-1' || task.label.toLowerCase().includes('hotel booking');

            let subtitle = task.subtext || '';
            if (!subtitle && isHotel) subtitle = 'Nov 20 – Nov 22, 2026 (2 Nights)';
            if (isGift && subtitle) subtitle += ' (+ wedding card)';

            const cardStyle = isGift && !task.checked
              ? 'bg-amber-50/90 border-amber-200/90'
              : task.checked
                ? 'bg-slate-50/80 border-slate-200/80'
                : 'bg-white border-slate-200';

            const btnStyle = task.checked
              ? 'bg-emerald-100 text-emerald-800 border-emerald-200'
              : isGift
                ? 'bg-white hover:bg-amber-100 text-amber-900 border-amber-300'
                : 'bg-amber-100 hover:bg-amber-200 text-amber-900 border-amber-300';

            const btnText = task.checked
              ? (isHotel ? '✓ Booked' : '✓ Done')
              : (isHotel ? '⏳ Pending' : isGift ? 'Mark Pulled' : 'Mark Done');

            return `
              <div class="group p-3 rounded-xl border flex items-center justify-between gap-2.5 transition ${cardStyle}">
                <div class="flex items-start gap-2.5 min-w-0 flex-1">
                  ${isGift ? '<span class="text-base leading-none mt-0.5 shrink-0">💵</span>' : ''}
                  <div class="min-w-0 flex-1">
                    <p class="text-xs font-bold truncate ${task.checked ? 'line-through text-slate-400' : isGift ? 'text-amber-950' : 'text-slate-800'}">
                      ${escapeHtml(task.label)}
                    </p>
                    ${subtitle ? `<p class="text-[11px] mt-0.5 leading-snug break-words ${task.checked ? 'text-slate-400' : isGift ? 'text-amber-800' : 'text-slate-500'}">${escapeHtml(subtitle)}</p>` : ''}
                  </div>
                </div>
                <div class="no-print shrink-0 flex items-center gap-1">
                  <button onclick="toggleItemById('${task.id}')" class="px-2.5 py-1.5 rounded-lg text-[11px] font-bold border transition cursor-pointer ${btnStyle}">
                    ${btnText}
                  </button>
                  <button onclick="openEditModal('${task.id}')" class="p-1 rounded-lg text-slate-400 hover:text-navy-900 hover:bg-slate-200/70 transition cursor-pointer" title="Edit task">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                  </button>
                  ${!['item-1', 'item-3'].includes(task.id) ? `
                    <button onclick="deleteItem('${task.id}')" class="p-1 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer" title="Remove task">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
                    </button>
                  ` : ''}
                </div>
              </div>
            `;
          }).join('');
        }
      }
    }

    function renderCategoryTabs() {
      const container = document.getElementById('category-tabs');
      const totalItems = state.items.length;
      const totalChecked = state.items.filter(i => i.checked).length;

      let html = `
        <button onclick="setActiveCategory('ALL')" class="shrink-0 inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition cursor-pointer border ${
          state.activeCategory === 'ALL'
            ? 'bg-navy-900 text-white border-navy-900 shadow-sm'
            : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
        }">
          <span>All Categories</span>
          <span class="px-1.5 py-0.5 rounded-md text-[11px] ${
            state.activeCategory === 'ALL' ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600'
          }">${totalChecked}/${totalItems}</span>
        </button>
      `;

      CATEGORIES.forEach(cat => {
        const catItems = state.items.filter(i => i.category === cat.id);
        const catChecked = catItems.filter(i => i.checked).length;
        const isActive = state.activeCategory === cat.id;
        const allDone = catItems.length > 0 && catChecked === catItems.length;

        html += `
          <button onclick="setActiveCategory('${escapeQuotes(cat.id)}')" class="shrink-0 inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition cursor-pointer border ${
            isActive
              ? 'bg-navy-900 text-white border-navy-900 shadow-sm'
              : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
          }">
            <span>${cat.icon}</span>
            <span>${cat.id}</span>
            <span class="px-1.5 py-0.5 rounded-md text-[11px] ${
              isActive
                ? 'bg-white/20 text-white'
                : allDone
                  ? 'bg-emerald-100 text-emerald-700'
                  : 'bg-slate-100 text-slate-600'
            }">${catChecked}/${catItems.length}</span>
          </button>
        `;
      });

      container.innerHTML = html;
    }

    function renderChecklist() {
      const container = document.getElementById('checklist-container');
      const searchInput = document.getElementById('search-input');
      const query = searchInput.value.trim().toLowerCase();
      document.getElementById('clear-search-btn').classList.toggle('hidden', query.length === 0);

      renderCategoryTabs();
      updateProgressUI();

      const visibleCategories = state.activeCategory === 'ALL'
        ? CATEGORIES
        : CATEGORIES.filter(c => c.id === state.activeCategory);

      let html = '';
      let totalRenderedItems = 0;

      visibleCategories.forEach(cat => {
        const allCatItems = state.items.filter(i => i.category === cat.id);
        const checkedCount = allCatItems.filter(i => i.checked).length;
        const allCatChecked = allCatItems.length > 0 && checkedCount === allCatItems.length;

        const filteredItems = allCatItems.filter(item => {
          if (state.hideCompleted && item.checked) return false;
          if (query) {
            const matchLabel = item.label.toLowerCase().includes(query);
            const matchSub = (item.subtext || '').toLowerCase().includes(query);
            const matchCat = item.category.toLowerCase().includes(query);
            return matchLabel || matchSub || matchCat;
          }
          return true;
        });

        if (filteredItems.length === 0 && (query || state.hideCompleted) && state.activeCategory === 'ALL') {
          return;
        }

        totalRenderedItems += filteredItems.length;
        const isKidsCat = cat.id === "Kids' Packing (Per Child)";

        html += `
          <div class="bg-white rounded-2xl shadow-sm border border-slate-200/90 overflow-hidden print-card">
            <div class="px-5 py-4 bg-slate-50/90 border-b border-slate-200/80 flex flex-wrap items-center justify-between gap-3">
              <div class="flex items-center gap-3">
                <span class="w-9 h-9 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-lg shadow-2xs">${cat.icon}</span>
                <div>
                  <div class="flex items-center gap-2.5">
                    <h3 class="font-bold text-slate-900 text-base">${cat.id}</h3>
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${
                      allCatChecked ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200/80 text-slate-700'
                    }">${checkedCount} / ${allCatItems.length}</span>
                  </div>
                  ${isKidsCat ? `<p class="text-xs text-amber-700 font-medium mt-0.5">Quantities listed are <strong>per child</strong> (4 kids: Adham, Sulaiman, Yasin, Saif-Eddine)</p>` : ''}
                </div>
              </div>

              <div class="flex flex-wrap items-center gap-2 no-print">
                ${isKidsCat ? `
                  <div class="inline-flex rounded-xl bg-slate-200/70 p-0.5 text-xs font-semibold">
                    <button onclick="setKidMode('MASTER')" class="px-2.5 py-1 rounded-lg transition cursor-pointer ${state.kidMode === 'MASTER' ? 'bg-white text-navy-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'}">Master List</button>
                    <button onclick="setKidMode('PER_CHILD')" class="px-2.5 py-1 rounded-lg transition cursor-pointer ${state.kidMode === 'PER_CHILD' ? 'bg-white text-navy-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'}">Track Each Kid</button>
                  </div>
                ` : ''}
                <button onclick="toggleCategoryAll('${escapeQuotes(cat.id)}')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold transition cursor-pointer">
                  ${allCatChecked ? 'Uncheck Category' : 'Check Category'}
                </button>
                <button onclick="openItemModal('${escapeQuotes(cat.id)}')" class="px-2.5 py-1.5 rounded-xl bg-lagoon-50 hover:bg-lagoon-100 text-lagoon-700 border border-lagoon-200 text-xs font-bold transition cursor-pointer" title="Add item to ${cat.id}">
                  + Add
                </button>
              </div>
            </div>

            <div class="divide-y divide-slate-100">
              ${
                filteredItems.length === 0
                  ? `<div class="p-6 text-center text-sm text-slate-400">No items match your current filter in this category.</div>`
                  : filteredItems.map(item => renderItemRow(item, isKidsCat)).join('')
              }
            </div>
          </div>
        `;
      });

      if (totalRenderedItems === 0) {
        html = `
          <div class="bg-white rounded-2xl border border-slate-200 p-10 text-center space-y-3">
            <div class="text-3xl">🧳</div>
            <h3 class="font-bold text-slate-800 text-base">No checklist items to show</h3>
            <p class="text-sm text-slate-500 max-w-md mx-auto">
              ${state.hideCompleted ? 'All items in this view are completed! Uncheck "Hide Completed" to see them.' : 'No items matched your search query.'}
            </p>
            <button onclick="resetFilters()" class="px-4 py-2 rounded-xl bg-navy-900 text-white text-xs font-bold cursor-pointer">Clear Filters</button>
          </div>
        `;
      }

      container.innerHTML = html;
    }

    function renderItemRow(item, isKidsCat) {
      const kidMap = isKidsCat ? (state.kidProgress[item.id] || {}) : null;

      return `
        <div class="group px-5 py-3.5 hover:bg-slate-50/80 transition flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${item.checked ? 'item-checked bg-slate-50/40' : ''}">
          <div class="flex items-start gap-3.5 flex-1 min-w-0">
            <input
              type="checkbox"
              ${item.checked ? 'checked' : ''}
              onchange="toggleItemById('${item.id}')"
              class="custom-checkbox mt-0.5"
              aria-label="Mark ${escapeHtml(item.label)} as completed"
            />
            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                <span onclick="toggleItemById('${item.id}')" class="item-label font-semibold text-sm sm:text-[15px] text-slate-800 cursor-pointer select-none">
                  ${escapeHtml(item.label)}
                </span>
                ${isKidsCat ? `<span class="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-amber-100/80 text-amber-800">× 4 Kids</span>` : ''}
              </div>
              ${item.subtext ? `<p class="item-subtext text-xs text-slate-500 mt-1 leading-relaxed break-words">${escapeHtml(item.subtext)}</p>` : ''}

              ${isKidsCat && state.kidMode === 'PER_CHILD' ? `
                <div class="flex flex-wrap items-center gap-1.5 mt-2.5 no-print">
                  ${KIDS_NAMES.map(kid => {
                    const isKidDone = Boolean(kidMap[kid]);
                    return `
                      <button
                        type="button"
                        onclick="toggleKidItem('${item.id}', '${kid}')"
                        class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer ${
                          isKidDone
                            ? 'bg-lagoon-600 text-white border-lagoon-600 shadow-2xs'
                            : 'bg-white text-slate-600 border-slate-200 hover:border-lagoon-400'
                        }"
                      >
                        <span>${isKidDone ? '✓' : '○'}</span>
                        <span>${kid}</span>
                      </button>
                    `;
                  }).join('')}
                </div>
              ` : ''}
            </div>
          </div>

          <div class="flex items-center gap-1.5 self-end sm:self-center opacity-100 sm:opacity-0 sm:group-hover:opacity-100 focus-within:opacity-100 transition no-print">
            <button onclick="openEditModal('${item.id}')" class="p-1.5 rounded-lg text-slate-400 hover:text-navy-900 hover:bg-slate-200/70 transition cursor-pointer" title="Edit item">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            </button>
            <button onclick="deleteItem('${item.id}')" class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer" title="Delete item">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </div>
      `;
    }

    function toggleItemById(id) {
      const item = state.items.find(i => i.id === id);
      if (!item) return;
      item.checked = !item.checked;

      if (item.category === "Kids' Packing (Per Child)") {
        if (!state.kidProgress[item.id]) state.kidProgress[item.id] = {};
        KIDS_NAMES.forEach(kid => {
          state.kidProgress[item.id][kid] = item.checked;
        });
      }

      saveState();
      renderChecklist();
    }

    function toggleKidItem(itemId, kidName) {
      const item = state.items.find(i => i.id === itemId);
      if (!item) return;
      if (!state.kidProgress[itemId]) state.kidProgress[itemId] = {};

      state.kidProgress[itemId][kidName] = !state.kidProgress[itemId][kidName];
      const allKidsDone = KIDS_NAMES.every(k => Boolean(state.kidProgress[itemId][k]));
      item.checked = allKidsDone;

      saveState();
      renderChecklist();
    }

    function toggleCategoryAll(categoryName) {
      const catItems = state.items.filter(i => i.category === categoryName);
      if (catItems.length === 0) return;
      const shouldCheck = !catItems.every(i => i.checked);

      catItems.forEach(item => {
        item.checked = shouldCheck;
        if (item.category === "Kids' Packing (Per Child)") {
          if (!state.kidProgress[item.id]) state.kidProgress[item.id] = {};
          KIDS_NAMES.forEach(k => state.kidProgress[item.id][k] = shouldCheck);
        }
      });

      saveState();
      renderChecklist();
      showToast(`${shouldCheck ? 'Checked' : 'Unchecked'} all items in ${categoryName}`);
    }

    function setActiveCategory(cat) {
      state.activeCategory = cat;
      saveState();
      renderChecklist();
    }

    function setKidMode(mode) {
      state.kidMode = mode;
      saveState();
      renderChecklist();
    }

    function toggleHideCompleted() {
      state.hideCompleted = document.getElementById('hide-completed-toggle').checked;
      saveState();
      renderChecklist();
    }

    function clearSearch() {
      document.getElementById('search-input').value = '';
      renderChecklist();
    }

    function resetFilters() {
      state.activeCategory = 'ALL';
      state.hideCompleted = false;
      document.getElementById('hide-completed-toggle').checked = false;
      document.getElementById('search-input').value = '';
      saveState();
      renderChecklist();
    }

    function toggleLogistics() {
      state.logisticsCollapsed = !state.logisticsCollapsed;
      applyLogisticsCollapseUI();
      saveState();
    }

    function applyLogisticsCollapseUI() {
      const body = document.getElementById('logistics-body');
      const label = document.getElementById('toggle-logistics-label');
      const icon = document.getElementById('toggle-logistics-icon');
      if (state.logisticsCollapsed) {
        body.classList.add('hidden');
        label.textContent = 'Show Details';
        icon.style.transform = 'rotate(180deg)';
      } else {
        body.classList.remove('hidden');
        label.textContent = 'Hide Details';
        icon.style.transform = 'rotate(0deg)';
      }
    }

    function openItemModal(defaultCat = null) {
      document.getElementById('modal-title').textContent = 'Add New Checklist Item';
      document.getElementById('edit-item-id').value = '';
      document.getElementById('item-label-input').value = '';
      document.getElementById('item-subtext-input').value = '';
      const targetCat = defaultCat || (state.activeCategory !== 'ALL' ? state.activeCategory : "Travel, Bookings & Wedding");
      document.getElementById('item-category-input').value = targetCat;

      const modal = document.getElementById('item-modal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      setTimeout(() => document.getElementById('item-label-input').focus(), 50);
    }

    function openEditModal(id) {
      const item = state.items.find(i => i.id === id);
      if (!item) return;
      document.getElementById('modal-title').textContent = 'Edit Checklist Item';
      document.getElementById('edit-item-id').value = item.id;
      document.getElementById('item-category-input').value = item.category;
      document.getElementById('item-label-input').value = item.label;
      document.getElementById('item-subtext-input').value = item.subtext || '';

      const modal = document.getElementById('item-modal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      setTimeout(() => document.getElementById('item-label-input').focus(), 50);
    }

    function closeItemModal() {
      const modal = document.getElementById('item-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function saveItemForm(e) {
      e.preventDefault();
      const editId = document.getElementById('edit-item-id').value;
      const category = document.getElementById('item-category-input').value;
      const label = document.getElementById('item-label-input').value.trim();
      const subtext = document.getElementById('item-subtext-input').value.trim();

      if (!label) return;

      if (editId) {
        const existing = state.items.find(i => i.id === editId);
        if (existing) {
          existing.category = category;
          existing.label = label;
          existing.subtext = subtext;
          showToast('Checklist item updated');
        }
      } else {
        const newId = 'custom-' + Date.now();
        state.items.push({
          id: newId,
          category,
          label,
          subtext,
          checked: false
        });
        showToast(`Added "${label}" to ${category}`);
      }

      ensureKidProgressStructure();
      saveState();
      closeItemModal();
      renderChecklist();
    }

    function deleteItem(id) {
      const item = state.items.find(i => i.id === id);
      if (!item) return;
      state.items = state.items.filter(i => i.id !== id);
      delete state.kidProgress[id];
      saveState();
      renderChecklist();
      showToast(`Removed "${item.label}"`);
    }

    function confirmAction(type) {
      const modal = document.getElementById('confirm-modal');
      const title = document.getElementById('confirm-title');
      const msg = document.getElementById('confirm-message');
      const btn = document.getElementById('confirm-proceed-btn');

      if (type === 'reset') {
        title.textContent = 'Reset All Checkmarks?';
        msg.textContent = 'This will uncheck every item on your California trip checklist while keeping your custom items.';
        btn.onclick = () => {
          state.items.forEach(i => i.checked = false);
          Object.keys(state.kidProgress).forEach(itemId => {
            KIDS_NAMES.forEach(k => state.kidProgress[itemId][k] = false);
          });
          saveState();
          renderChecklist();
          closeConfirmModal();
          showToast('All checkmarks cleared');
        };
      } else if (type === 'restore') {
        title.textContent = 'Restore Default 35-Item List?';
        msg.textContent = 'This will revert any custom additions, deletions, or text edits back to your original California trip list.';
        btn.onclick = () => {
          state.items = JSON.parse(JSON.stringify(DEFAULT_ITEMS));
          state.kidProgress = {};
          ensureKidProgressStructure();
          saveState();
          renderChecklist();
          closeConfirmModal();
          showToast('Restored default trip checklist');
        };
      }

      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeConfirmModal() {
      const modal = document.getElementById('confirm-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function openExportModal() {
      const lines = [
        'CALIFORNIA TRIP PLANNER & CHECKLIST (NOV 20–22, 2026)',
        '====================================================',
        'FLIGHTS:',
        '• Outbound: Delta 0752 (JFK → LAX) | Thu, Nov 19 at 8:55 PM EST | Conf: GUT49I',
        '• Return: JetBlue 0524 (LAX T1 → JFK) | Sun, Nov 22 at 2:30 PM PST | Conf: QYYWWI',
        '',
        'CAR RENTAL:',
        '• Budget Rent A Car | Conf #07264298US6 | Lincoln Navigator or similar',
        '• Pickup: Fri, Nov 20 at 1:30 AM | Dropoff: Sun, Nov 22 at 3:00 PM',
        '• Location: LAX ConRAC, 5251 W 98th St, Los Angeles, CA 90045 | Total: $464.33',
        '====================================================',
        ''
      ];

      CATEGORIES.forEach(cat => {
        const catItems = state.items.filter(i => i.category === cat.id);
        if (catItems.length > 0) {
          lines.push(`${cat.icon} ${cat.id.toUpperCase()}`);
          catItems.forEach(item => {
            const box = item.checked ? '[x]' : '[ ]';
            lines.push(`  ${box} ${item.label}${item.subtext ? ` — ${item.subtext}` : ''}`);
          });
          lines.push('');
        }
      });

      document.getElementById('export-textarea').value = lines.join('\n');
      const modal = document.getElementById('export-modal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeExportModal() {
      const modal = document.getElementById('export-modal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function copyExportText() {
      const textarea = document.getElementById('export-textarea');
      textarea.select();
      try {
        document.execCommand('copy');
        showToast('Full checklist copied to clipboard!');
      } catch (e) {
        showToast('Could not copy automatically—select and copy text manually.');
      }
    }

    function copyText(text, successMsg) {
      const tempInput = document.createElement('input');
      tempInput.value = text;
      document.body.appendChild(tempInput);
      tempInput.select();
      try {
        document.execCommand('copy');
        showToast(successMsg || `Copied: ${text}`);
      } catch (err) {
        showToast('Copy failed');
      }
      document.body.removeChild(tempInput);
    }

    function showToast(message) {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      toast.className = 'bg-navy-900 text-white text-xs font-semibold px-4 py-2.5 rounded-xl shadow-lg border border-white/10 flex items-center gap-2 transition-all duration-300 transform translate-y-2 opacity-0';
      toast.innerHTML = `<span class="text-lagoon-400">✓</span><span>${escapeHtml(message)}</span>`;
      container.appendChild(toast);

      requestAnimationFrame(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
      });

      setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
      }, 2600);
    }

    function escapeHtml(str) {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    }

    function escapeQuotes(str) {
      return str.replace(/'/g, "\\'");
    }

    window.addEventListener('DOMContentLoaded', () => {
      loadState();
      document.getElementById('hide-completed-toggle').checked = state.hideCompleted;
      applyLogisticsCollapseUI();
      updateCountdown();
      renderChecklist();
    });
  </script>
</body>
</html>"""

components.html(HTML_CONTENT, height=2200, scrolling=True)