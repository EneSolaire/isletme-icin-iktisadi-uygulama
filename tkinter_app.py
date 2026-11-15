import tkinter as tk
from tkinter import ttk


SECTOR_PROFILES = {
    "manufacturing": {"staffing": 12, "investment": 15, "automation": 10, "inventory": 12, "demand": 8},
    "retail": {"staffing": 10, "investment": 8, "automation": 5, "inventory": 18, "demand": 14},
    "services": {"staffing": 18, "investment": 7, "automation": 12, "inventory": 6, "demand": 10},
    "technology": {"staffing": 15, "investment": 22, "automation": 20, "inventory": 4, "demand": 16},
    "construction": {"staffing": 14, "investment": 18, "automation": 9, "inventory": 10, "demand": 12},
    "agriculture": {"staffing": 11, "investment": 10, "automation": 8, "inventory": 14, "demand": 9},
}

SIZE_PROFILES = {
    "micro": {"scale": 0.8, "capital": 6, "staffing": 8},
    "small": {"scale": 1, "capital": 10, "staffing": 10},
    "medium": {"scale": 1.2, "capital": 14, "staffing": 14},
    "large": {"scale": 1.5, "capital": 20, "staffing": 18},
}


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def get_scenario_title(score):
    if score >= 75:
        return "Yüksek stresli büyüme senaryosu"
    if score >= 55:
        return "Dengeli ancak riskli piyasa"
    if score >= 35:
        return "Dengeli büyüme senaryosu"
    return "Güçlü yatırım fırsatı senaryosu"


def build_recommendations(data):
    recommendations = []
    labor_need = data["labor_need"]
    working_capital_need = data["working_capital_need"]
    capex_need = data["capex_need"]
    automation_need = data["automation_need"]
    inventory_need = data["inventory_need"]
    risk_index = data["risk_index"]
    inflation = data["inflation"]
    interest_rate = data["interest_rate"]
    sector = data["sector"]
    size = data["size"]

    if labor_need >= 60:
        recommendations.append("İşgücü planlamasında esnek çalışma modelleri ve kısa vadeli personel tahsisi oluşturun.")
    else:
        recommendations.append("İstihdam artışını kontrollü şekilde planlayıp, yetenek geliştirme yatırımı önceliklendirin.")

    if working_capital_need >= 65:
        recommendations.append("Nakit akışı ihtiyacını azaltmak için stok ve alacak yönetimini sıkılaştırın; ödeme koşullarını yeniden düzenleyin.")
    else:
        recommendations.append("Daha yüksek likidite için operasyonel giderleri ve stok dönüşümünü optimize edin.")

    if capex_need >= 60:
        recommendations.append("Yatırım planlamasında üretim kapasitesi artırımı ve teknoloji altyapısı için ayrılan bütçeyi artırın.")
    else:
        recommendations.append("Büyüme için odaklı yatırım öncelikleri belirleyip, gereksiz sermaye harcamalarından kaçının.")

    if automation_need >= 55:
        recommendations.append("Maliyet baskısını azaltmak için otomasyon, veri analitiği ve dijital operasyon araçlarına yatırım yapın.")

    if inventory_need >= 60:
        recommendations.append("Talep dalgalanmasına karşı stok seviyelerini daha esnek bir şekilde yönetin ve tedarik zincirini çeşitlendirin.")

    if risk_index >= 60:
        recommendations.append("Ekonomik riskleri dengelemek için finansal tampon oluşturup, senaryo bazlı bütçe planlaması uygulayın.")

    labels = {
        "manufacturing": "üretim",
        "retail": "perakende",
        "services": "hizmet",
        "technology": "teknoloji",
        "construction": "inşaat",
        "agriculture": "tarım",
    }

    recommendations.append(
        f"Mevcut {labels[sector]} sektörü ve {size} ölçek profiline göre, enflasyon {inflation:.1f}% ve faiz {interest_rate:.1f}% seviyelerinde finansal esneklik hedefleyin."
    )
    return recommendations


def compute_forecast(values):
    gdp_growth = float(values["gdp_growth"])
    inflation = float(values["inflation"])
    interest_rate = float(values["interest_rate"])
    unemployment = float(values["unemployment"])
    consumer_confidence = float(values["consumer_confidence"])
    sector_momentum = float(values["sector_momentum"])
    sector = values["sector"]
    size = values["company_size"]

    sector_profile = SECTOR_PROFILES[sector]
    size_profile = SIZE_PROFILES[size]

    demand_index = clamp(
        (gdp_growth * 7)
        + (consumer_confidence * 0.7)
        + (sector_momentum * 0.8)
        + (sector_profile["demand"] * 0.9)
        - (inflation * 1.4),
        0,
        100,
    )

    cost_pressure = clamp(
        (inflation * 2.1)
        + (interest_rate * 2.3)
        + (unemployment * 1.4)
        - (gdp_growth * 1.1),
        0,
        100,
    )

    risk_index = clamp(
        (cost_pressure * 0.5)
        + (abs(gdp_growth) * 4)
        + ((100 - consumer_confidence) * 0.5)
        + (unemployment * 1.8),
        0,
        100,
    )

    labor_need = clamp(
        22
        + (demand_index * 0.46)
        + sector_profile["staffing"]
        + size_profile["staffing"]
        - (unemployment * 0.7)
        - (cost_pressure * 0.12),
        0,
        100,
    )

    working_capital_need = clamp(
        28
        + (cost_pressure * 0.78)
        + (inflation * 0.8)
        + size_profile["capital"]
        + (sector_profile["inventory"] * 0.5),
        0,
        100,
    )

    capex_need = clamp(
        18
        + (demand_index * 0.42)
        + sector_profile["investment"]
        + (size_profile["scale"] * 12)
        - (cost_pressure * 0.15),
        0,
        100,
    )

    automation_need = clamp(
        20
        + (cost_pressure * 0.42)
        + ((100 - consumer_confidence) * 0.15)
        + sector_profile["automation"]
        + (interest_rate * 0.7),
        0,
        100,
    )

    inventory_need = clamp(
        15
        + sector_profile["inventory"]
        + (demand_index * 0.25)
        + (inflation * 0.35)
        - (consumer_confidence * 0.1),
        0,
        100,
    )

    overall_score = clamp(
        (labor_need + working_capital_need + capex_need + automation_need + inventory_need + risk_index) / 6,
        0,
        100,
    )

    return {
        "overall_score": overall_score,
        "scenario_title": get_scenario_title(overall_score),
        "labor_need": labor_need,
        "working_capital_need": working_capital_need,
        "capex_need": capex_need,
        "automation_need": automation_need,
        "inventory_need": inventory_need,
        "risk_index": risk_index,
        "demand_index": demand_index,
        "recommendations": build_recommendations({
            "labor_need": labor_need,
            "working_capital_need": working_capital_need,
            "capex_need": capex_need,
            "automation_need": automation_need,
            "inventory_need": inventory_need,
            "risk_index": risk_index,
            "inflation": inflation,
            "interest_rate": interest_rate,
            "sector": sector,
            "size": size,
        }),
    }


class ForecastApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ekonomik Durum Tabanlı İşletme İhtiyaç Tahmini")
        self.root.geometry("1180x760")
        self.root.minsize(1060, 700)
        self.root.configure(bg="#0b1220")

        self.variables = {
            "gdp_growth": tk.DoubleVar(value=2.5),
            "inflation": tk.DoubleVar(value=12.0),
            "interest_rate": tk.DoubleVar(value=9.0),
            "unemployment": tk.DoubleVar(value=8.5),
            "consumer_confidence": tk.DoubleVar(value=68),
            "sector_momentum": tk.DoubleVar(value=72),
            "sector": tk.StringVar(value="Üretim"),
            "company_size": tk.StringVar(value="Küçük"),
        }

        self.build_ui()
        self.update_all()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 16))

        ttk.Label(header, text="İşletme Planlama Aracı", font=("Segoe UI", 11, "bold"), foreground="#62d0ff").pack(anchor="w")
        ttk.Label(header, text="Ekonomik Durum Tabanlı İhtiyaç Tahmini", font=("Segoe UI", 24, "bold")).pack(anchor="w")

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        left = ttk.Frame(content, padding=18)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        right = ttk.Frame(content, padding=18)
        right.grid(row=0, column=1, sticky="nsew")

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        left_card = tk.Frame(left, bg="#111b2d", padx=20, pady=18, highlightthickness=1, highlightbackground="#2c3d5d")
        left_card.pack(fill="both", expand=True)
        ttk.Label(left_card, text="Ekonomik ve operasyonel veri", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 14))

        self.slider_rows = []
        for key, label_text, from_, to_, resolution in [
            ("gdp_growth", "GSYH Büyümesi (%)", -5, 10, 0.5),
            ("inflation", "Enflasyon (%)", 0, 25, 0.5),
            ("interest_rate", "Faiz Oranı (%)", 0, 25, 0.5),
            ("unemployment", "İşsizlik Oranı (%)", 2, 20, 0.5),
            ("consumer_confidence", "Tüketici Güveni", 20, 100, 1),
            ("sector_momentum", "Sektör Momentum", 0, 100, 1),
        ]:
            row = tk.Frame(left_card, bg="#111b2d", pady=8)
            row.pack(fill="x")
            label = tk.Label(row, text=label_text, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"), anchor="w")
            label.pack(anchor="w")
            scale = tk.Scale(
                row,
                from_=from_,
                to_=to_,
                resolution=resolution,
                orient="horizontal",
                variable=self.variables[key],
                bg="#111b2d",
                fg="#e2e8f0",
                highlightthickness=0,
                activebackground="#62d0ff",
                troughcolor="#24324e",
                bd=0,
                length=320,
                command=lambda _event=None, key=key: self.update_all(),
            )
            scale.pack(fill="x")
            value_label = tk.Label(row, text="0.0", bg="#111b2d", fg="#a8b5c7", font=("Segoe UI", 10, "bold"), anchor="e")
            value_label.pack(anchor="e")
            self.slider_rows.append((key, value_label))

        combo_row = tk.Frame(left_card, bg="#111b2d", pady=12)
        combo_row.pack(fill="x")
        ttk.Label(combo_row, text="İşletme Sektörü", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        sector_combo = ttk.Combobox(combo_row, textvariable=self.variables["sector"], values=[
            "Üretim",
            "Perakende",
            "Hizmet",
            "Teknoloji",
            "İnşaat",
            "Tarım",
        ])
        sector_combo.pack(fill="x", pady=6)
        sector_combo.bind("<<ComboboxSelected>>", lambda event: self.update_all())

        combo_row2 = tk.Frame(left_card, bg="#111b2d", pady=12)
        combo_row2.pack(fill="x")
        ttk.Label(combo_row2, text="Firma Büyüklüğü", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        size_combo = ttk.Combobox(combo_row2, textvariable=self.variables["company_size"], values=[
            "Mikro",
            "Küçük",
            "Orta",
            "Büyük",
        ])
        size_combo.pack(fill="x", pady=6)
        size_combo.bind("<<ComboboxSelected>>", lambda event: self.update_all())

        right_card = tk.Frame(right, bg="#111b2d", padx=20, pady=18, highlightthickness=1, highlightbackground="#2c3d5d")
        right_card.pack(fill="both", expand=True)

        summary = tk.Frame(right_card, bg="#111b2d")
        summary.pack(fill="x", pady=(0, 16))
        ttk.Label(summary, text="Tahmin özeti", foreground="#a8b5c7", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.scenario_title = ttk.Label(summary, text="Dengeli büyüme senaryosu", font=("Segoe UI", 18, "bold"))
        self.scenario_title.pack(anchor="w")

        score_frame = tk.Frame(right_card, bg="#111b2d")
        score_frame.pack(fill="x", pady=(0, 18))

        self.overall_score = tk.Label(score_frame, text="0", bg="#111b2d", fg="#62d0ff", font=("Segoe UI", 24, "bold"), padx=18, pady=16)
        self.overall_score.pack(side="right")

        cards = tk.Frame(right_card, bg="#111b2d")
        cards.pack(fill="x")
        self.metric_labels = {}
        metric_specs = [
            ("labor_need", "İşgücü ihtiyacı", "#62d0ff"),
            ("working_capital_need", "Çalışma sermayesi", "#fbbf24"),
            ("capex_need", "Yatırım kapasitesi", "#34d399"),
            ("automation_need", "Teknoloji / otomasyon", "#7dd3fc"),
        ]

        for index, (key, label_text, color) in enumerate(metric_specs):
            frame = tk.Frame(cards, bg="#172438", padx=12, pady=12, highlightthickness=1, highlightbackground="#2d3f61")
            frame.grid(row=index // 2, column=index % 2, sticky="nsew", padx=8, pady=8)
            cards.grid_columnconfigure(0, weight=1)
            cards.grid_columnconfigure(1, weight=1)
            tk.Label(frame, text=label_text, bg="#172438", fg="#a8b5c7", font=("Segoe UI", 9, "bold")).pack(anchor="w")
            value = tk.Label(frame, text="0", bg="#172438", fg=color, font=("Segoe UI", 24, "bold"))
            value.pack(anchor="w", pady=(6, 0))
            self.metric_labels[key] = value

        bars_frame = tk.Frame(right_card, bg="#111b2d", pady=10)
        bars_frame.pack(fill="x", pady=(18, 0))

        self.bar_vars = {
            "inventory_need": {"label": tk.Label(bars_frame, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"), anchor="w"), "canvas": tk.Canvas(bars_frame, width=300, height=18, bg="#111b2d", highlightthickness=0), "value": tk.Label(bars_frame, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"))},
            "risk_index": {"label": tk.Label(bars_frame, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"), anchor="w"), "canvas": tk.Canvas(bars_frame, width=300, height=18, bg="#111b2d", highlightthickness=0), "value": tk.Label(bars_frame, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"))},
            "demand_index": {"label": tk.Label(bars_frame, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"), anchor="w"), "canvas": tk.Canvas(bars_frame, width=300, height=18, bg="#111b2d", highlightthickness=0), "value": tk.Label(bars_frame, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"))},
        }

        bar_configs = [
            ("inventory_need", "Stok ve envanter", "#34d399"),
            ("risk_index", "Risk yönetimi", "#fbbf24"),
            ("demand_index", "Satış / talep desteği", "#7dd3fc"),
        ]

        for index, (key, bar_text, color) in enumerate(bar_configs):
            row = tk.Frame(bars_frame, bg="#111b2d", pady=8)
            row.pack(fill="x")
            label = tk.Label(row, text=bar_text, bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"), width=18, anchor="w")
            label.pack(side="left")
            canvas = tk.Canvas(row, width=420, height=18, bg="#111b2d", highlightthickness=0)
            canvas.pack(side="left", padx=(8, 8), fill="x", expand=True)
            value = tk.Label(row, text="0", bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 10, "bold"), width=4)
            value.pack(side="left")
            self.bar_vars[key] = {"canvas": canvas, "value": value, "color": color}

        recommendation_label = tk.Label(right_card, text="Önerilen eylemler", bg="#111b2d", fg="#e2e8f0", font=("Segoe UI", 12, "bold"))
        recommendation_label.pack(anchor="w", pady=(18, 10))
        self.recommendation_text = tk.Text(right_card, height=10, wrap="word", bg="#0d1728", fg="#dbe6f2", insertbackground="#dbe6f2", relief="flat")
        self.recommendation_text.pack(fill="both", expand=True)
        self.recommendation_text.configure(state="disabled")

    def update_all(self):
        sector_map = {
            "Üretim": "manufacturing",
            "Perakende": "retail",
            "Hizmet": "services",
            "Teknoloji": "technology",
            "İnşaat": "construction",
            "Tarım": "agriculture",
        }
        size_map = {
            "Mikro": "micro",
            "Küçük": "small",
            "Orta": "medium",
            "Büyük": "large",
        }

        values = {
            "gdp_growth": self.variables["gdp_growth"].get(),
            "inflation": self.variables["inflation"].get(),
            "interest_rate": self.variables["interest_rate"].get(),
            "unemployment": self.variables["unemployment"].get(),
            "consumer_confidence": self.variables["consumer_confidence"].get(),
            "sector_momentum": self.variables["sector_momentum"].get(),
            "sector": sector_map.get(self.variables["sector"].get(), "manufacturing"),
            "company_size": size_map.get(self.variables["company_size"].get(), "small"),
        }

        for key, label in self.slider_rows:
            label.config(text=f"{self.variables[key].get():.1f}")

        result = compute_forecast(values)
        self.scenario_title.config(text=result["scenario_title"])
        self.overall_score.config(text=str(round(result["overall_score"])))

        widgets = {
            "labor_need": result["labor_need"],
            "working_capital_need": result["working_capital_need"],
            "capex_need": result["capex_need"],
            "automation_need": result["automation_need"],
        }
        for key, value in widgets.items():
            self.metric_labels[key].config(text=str(round(value)))

        bar_map = {
            "inventory_need": result["inventory_need"],
            "risk_index": result["risk_index"],
            "demand_index": result["demand_index"],
        }

        for key, value in bar_map.items():
            canvas = self.bar_vars[key]["canvas"]
            color = self.bar_vars[key]["color"]
            canvas.delete("all")
            width = int(max(0, min(100, value)))
            canvas.create_rectangle(0, 0, 400, 18, fill="#22314a", outline="")
            canvas.create_rectangle(0, 0, (width / 100) * 400, 18, fill=color, outline="")
            self.bar_vars[key]["value"].config(text=str(round(value)))

        recommendations = "\n• ".join(result["recommendations"])
        self.recommendation_text.configure(state="normal")
        self.recommendation_text.delete("1.0", "end")
        self.recommendation_text.insert("1.0", "• " + recommendations.replace("\n• ", "\n• "))
        self.recommendation_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    ForecastApp(root)
    root.mainloop()
