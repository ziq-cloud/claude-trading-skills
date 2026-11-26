"""UI translations: English, Bahasa Melayu, Tamil, Simplified Chinese.

Every key maps to one value per language. Values are str.format templates (placeholders
must match across languages; tests enforce this) or, for quiz options, lists.
Skill output (breadth signals, catalog summaries) comes from the skills in English.
"""

from __future__ import annotations

LANGUAGES = {"en": "English", "ms": "Bahasa Melayu", "ta": "தமிழ்", "zh": "中文"}
DEFAULT_LANG = "en"


def L(en, ms, ta, zh):  # noqa: N802 - short constructor for the table below
    return {"en": en, "ms": ms, "ta": ta, "zh": zh}


STRINGS: dict[str, dict] = {
    # ------------------------------------------------------------------ app / navigation
    "app.language": L("Language", "Bahasa", "மொழி", "语言"),
    "nav.train": L("Train", "Latihan", "பயிற்சி", "训练"),
    "nav.tools": L("Tools", "Alatan", "கருவிகள்", "工具"),
    "nav.home": L("Home", "Laman Utama", "முகப்பு", "首页"),
    "nav.learn": L("Learning Path", "Laluan Pembelajaran", "கற்றல் பாதை", "学习路径"),
    "nav.replay": L("Chart Replay", "Ulang Tayang Carta", "விளக்கப்பட மறுஇயக்கம்", "图表回放"),
    "nav.demo": L("Demo Account", "Akaun Demo", "டெமோ கணக்கு", "模拟账户"),
    "nav.chart": L("Price Chart", "Carta Harga", "விலை விளக்கப்படம்", "价格图表"),
    "nav.sizer": L("Position Sizer", "Kalkulator Saiz Posisi", "நிலை அளவு கணிப்பான்", "仓位计算器"),
    "nav.breadth": L("Market Breadth", "Keluasan Pasaran", "சந்தை அகலம்", "市场广度"),
    "nav.catalog": L("Skill Catalog", "Katalog Skill", "திறன் பட்டியல்", "技能目录"),
    "side.level": L(
        "Level {n}: {name}", "Tahap {n}: {name}", "நிலை {n}: {name}", "第 {n} 级：{name}"
    ),
    "side.disclaimer": L(
        "For education and analysis only — not financial advice. "
        "Always verify numbers before placing a trade.",
        "Untuk pendidikan dan analisis sahaja — bukan nasihat kewangan. "
        "Sentiasa semak nombor sebelum membuat dagangan.",
        "கல்வி மற்றும் பகுப்பாய்வுக்கு மட்டுமே — இது நிதி ஆலோசனை அல்ல. "
        "வர்த்தகம் செய்வதற்கு முன் எண்களை எப்போதும் சரிபார்க்கவும்.",
        "仅供教育和分析之用，不构成投资建议。下单前请务必核对数字。",
    ),
    "common.entry": L("entry", "masuk", "நுழைவு", "入场"),
    "common.stop": L("Stop-loss", "Henti rugi", "நிறுத்த இழப்பு", "止损"),
    "common.target": L("Target", "Sasaran", "இலக்கு", "目标"),
    "common.win_rate": L("Win rate", "Kadar menang", "வெற்றி விகிதம்", "胜率"),
    "common.expectancy": L("Expectancy", "Jangkaan", "எதிர்பார்ப்பு", "期望值"),
    "common.ticker": L("Ticker", "Simbol saham", "பங்கு குறியீடு", "股票代码"),
    "common.price_error": L(
        "Could not load price data. Set TWELVEDATA_API_KEY or install yfinance.",
        "Data harga tidak dapat dimuatkan. Tetapkan TWELVEDATA_API_KEY atau pasang yfinance.",
        "விலை தரவை ஏற்ற முடியவில்லை. TWELVEDATA_API_KEY அமைக்கவும் அல்லது yfinance நிறுவவும்.",
        "无法加载价格数据。请设置 TWELVEDATA_API_KEY 或安装 yfinance。",
    ),
    # ------------------------------------------------------------------ home
    "home.intro": L(
        "Learn to trade step by step, from zero to an advanced, rule-based process, "
        "with virtual money first.",
        "Belajar trading langkah demi langkah, dari kosong hingga proses berasaskan peraturan "
        "tahap lanjutan, dengan wang maya dahulu.",
        "பூஜ்ஜியத்திலிருந்து மேம்பட்ட, விதிமுறை அடிப்படையிலான செயல்முறை வரை படிப்படியாக "
        "வர்த்தகம் கற்றுக்கொள்ளுங்கள் — முதலில் மெய்நிகர் பணத்துடன்.",
        "从零开始，循序渐进地学习交易，直到掌握进阶的规则化流程——先用虚拟资金练习。",
    ),
    "home.you_are": L(
        "**You are at Level {n}: {name}** — {goal}",
        "**Anda di Tahap {n}: {name}** — {goal}",
        "**நீங்கள் நிலை {n}: {name} இல் உள்ளீர்கள்** — {goal}",
        "**您目前处于第 {n} 级：{name}** — {goal}",
    ),
    "home.next": L(
        "Next: {unlock}", "Seterusnya: {unlock}", "அடுத்து: {unlock}", "下一步：{unlock}"
    ),
    "home.continue": L(
        "Continue on the Learning Path →",
        "Teruskan Laluan Pembelajaran →",
        "கற்றல் பாதையைத் தொடரவும் →",
        "继续学习路径 →",
    ),
    "home.m_skills": L(
        "Skills in catalog", "Skill dalam katalog", "பட்டியலில் உள்ள திறன்கள்", "目录中的技能"
    ),
    "home.m_free": L(
        "Work without a paid API",
        "Tanpa API berbayar",
        "கட்டண API இல்லாமல் இயங்கும்",
        "无需付费 API",
    ),
    "home.m_paid": L(
        "Need FMP / FINVIZ / Alpaca",
        "Perlu FMP / FINVIZ / Alpaca",
        "FMP / FINVIZ / Alpaca தேவை",
        "需要 FMP / FINVIZ / Alpaca",
    ),
    "home.tools": L("What you can do", "Apa yang boleh dibuat", "நீங்கள் செய்யக்கூடியவை", "功能一览"),
    "home.desc.replay": L(
        "Practise entries on hidden historical charts.",
        "Latih kemasukan pada carta sejarah yang tersembunyi.",
        "மறைக்கப்பட்ட வரலாற்று விளக்கப்படங்களில் நுழைவுகளைப் பயிற்சி செய்யுங்கள்.",
        "在隐藏未来走势的历史图表上练习入场。",
    ),
    "home.desc.demo": L(
        "Paper trade with virtual money on real prices.",
        "Dagangan kertas dengan wang maya pada harga sebenar.",
        "உண்மையான விலைகளில் மெய்நிகர் பணத்துடன் காகித வர்த்தகம்.",
        "用虚拟资金按真实价格进行模拟交易。",
    ),
    "home.desc.chart": L(
        "Candles, SMA 20/50/200, RSI and ATR for any ticker.",
        "Lilin, SMA 20/50/200, RSI dan ATR untuk mana-mana saham.",
        "எந்தப் பங்குக்கும் மெழுகுவர்த்திகள், SMA 20/50/200, RSI மற்றும் ATR.",
        "任意股票的K线、SMA 20/50/200、RSI 和 ATR。",
    ),
    "home.desc.sizer": L(
        "Risk-based share count: fixed %, ATR or Kelly.",
        "Bilangan saham berasaskan risiko: % tetap, ATR atau Kelly.",
        "இடர் அடிப்படையிலான பங்கு எண்ணிக்கை: நிலையான %, ATR அல்லது Kelly.",
        "基于风险的股数：固定比例、ATR 或凯利公式。",
    ),
    "home.desc.breadth": L(
        "0–100 market health score from public data.",
        "Skor kesihatan pasaran 0–100 daripada data awam.",
        "பொது தரவிலிருந்து 0–100 சந்தை ஆரோக்கிய மதிப்பெண்.",
        "基于公开数据的 0–100 市场健康评分。",
    ),
    "home.desc.catalog": L(
        "Browse all skills, filter by category and API need.",
        "Semak semua skill, tapis mengikut kategori dan keperluan API.",
        "அனைத்து திறன்களையும் பார்க்கவும்; வகை மற்றும் API தேவைப்படி வடிகட்டவும்.",
        "浏览所有技能，按类别和 API 需求筛选。",
    ),
    "home.path": L(
        "Path: **Learning Path** (lessons + quiz) → **Chart Replay** (10 practice trades) → "
        "**Demo Account** (10 trades with positive expectancy) → advanced tools.",
        "Laluan: **Laluan Pembelajaran** (pelajaran + kuiz) → **Ulang Tayang Carta** "
        "(10 dagangan latihan) → **Akaun Demo** (10 dagangan dengan jangkaan positif) → "
        "alatan lanjutan.",
        "பாதை: **கற்றல் பாதை** (பாடங்கள் + வினாடி வினா) → **விளக்கப்பட மறுஇயக்கம்** "
        "(10 பயிற்சி வர்த்தகங்கள்) → **டெமோ கணக்கு** (நேர்மறை எதிர்பார்ப்புடன் 10 வர்த்தகங்கள்) "
        "→ மேம்பட்ட கருவிகள்.",
        "路线：**学习路径**（课程 + 测验）→ **图表回放**（10 笔练习交易）→ "
        "**模拟账户**（10 笔正期望值交易）→ 进阶工具。",
    ),
    # ------------------------------------------------------------------ levels
    "level.1.name": L("Beginner", "Permulaan", "தொடக்கநிலை", "入门"),
    "level.1.goal": L(
        "Learn to read a chart and understand why every trade needs a stop-loss.",
        "Belajar membaca carta dan faham kenapa setiap dagangan perlu henti rugi.",
        "விளக்கப்படத்தைப் படிக்கவும், ஒவ்வொரு வர்த்தகத்திற்கும் நிறுத்த இழப்பு ஏன் தேவை "
        "என்பதைப் புரிந்துகொள்ளவும் கற்றுக்கொள்ளுங்கள்.",
        "学会看图表，理解为什么每笔交易都需要止损。",
    ),
    "level.1.unlock": L(
        "Pass the basics quiz (80% or better).",
        "Lulus kuiz asas (80% atau lebih).",
        "அடிப்படை வினாடி வினாவில் தேர்ச்சி பெறுங்கள் (80% அல்லது அதற்கு மேல்).",
        "通过基础测验（80% 或以上）。",
    ),
    "level.2.name": L("Risk Control", "Kawalan Risiko", "இடர் கட்டுப்பாடு", "风险控制"),
    "level.2.goal": L(
        "Practise entries with a stop and a target on historical charts.",
        "Latih kemasukan dengan henti rugi dan sasaran pada carta sejarah.",
        "வரலாற்று விளக்கப்படங்களில் நிறுத்தம் மற்றும் இலக்குடன் நுழைவுகளைப் பயிற்சி செய்யுங்கள்.",
        "在历史图表上练习带止损和目标的入场。",
    ),
    "level.2.unlock": L(
        "Complete {n} Chart Replay trades.",
        "Lengkapkan {n} dagangan Ulang Tayang Carta.",
        "{n} விளக்கப்பட மறுஇயக்க வர்த்தகங்களை முடிக்கவும்.",
        "完成 {n} 笔图表回放交易。",
    ),
    "level.3.name": L("Trend & Context", "Trend & Konteks", "போக்கு & சூழல்", "趋势与环境"),
    "level.3.goal": L(
        "Trade the demo account on live prices and read the market backdrop first.",
        "Berdagang dalam akaun demo pada harga semasa dan baca keadaan pasaran dahulu.",
        "நேரடி விலைகளில் டெமோ கணக்கில் வர்த்தகம் செய்யுங்கள்; முதலில் சந்தை சூழலைப் படியுங்கள்.",
        "用实时价格在模拟账户交易，并先判断大盘环境。",
    ),
    "level.3.unlock": L(
        "Close {n} demo trades with positive expectancy.",
        "Tutup {n} dagangan demo dengan jangkaan positif.",
        "நேர்மறை எதிர்பார்ப்புடன் {n} டெமோ வர்த்தகங்களை மூடவும்.",
        "以正期望值平仓 {n} 笔模拟交易。",
    ),
    "level.4.name": L("Advanced", "Lanjutan", "மேம்பட்டது", "进阶"),
    "level.4.goal": L(
        "Use the screeners and setups to build a repeatable process.",
        "Gunakan screener dan setup untuk membina proses yang boleh diulang.",
        "மீண்டும் செய்யக்கூடிய செயல்முறையை உருவாக்க ஸ்கிரீனர்கள் மற்றும் அமைப்புகளைப் பயன்படுத்துங்கள்.",
        "使用选股器和交易形态，建立可重复的流程。",
    ),
    "level.4.unlock": L("Top level.", "Tahap tertinggi.", "உயர்ந்த நிலை.", "最高级别。"),
    # ------------------------------------------------------------------ lessons
    "lesson.candles.title": L("Candlesticks", "Lilin (candlestick)", "மெழுகுவர்த்தி வரைபடம்", "K线"),
    "lesson.candles.body": L(
        "Each candle is one period (here: one day). The **body** spans open to close; green "
        "means close > open, red means close < open. The **wicks** show the high and low. Long "
        "lower wicks mean buyers pushed price back up; long upper wicks mean sellers pushed it "
        "down.",
        "Setiap lilin ialah satu tempoh (di sini: satu hari). **Badan** lilin dari harga buka ke "
        "harga tutup; hijau bermaksud tutup > buka, merah bermaksud tutup < buka. **Sumbu** "
        "menunjukkan harga tertinggi dan terendah. Sumbu bawah panjang bermaksud pembeli menolak "
        "harga naik semula; sumbu atas panjang bermaksud penjual menolaknya turun.",
        "ஒவ்வொரு மெழுகுவர்த்தியும் ஒரு காலகட்டம் (இங்கே: ஒரு நாள்). **உடல்** திறப்பு முதல் "
        "முடிவு விலை வரை; பச்சை என்றால் முடிவு > திறப்பு, சிவப்பு என்றால் முடிவு < திறப்பு. "
        "**திரிகள்** அதிகபட்ச மற்றும் குறைந்தபட்ச விலையைக் காட்டும். நீண்ட கீழ் திரி வாங்குபவர்கள் "
        "விலையை மேலே தள்ளியதைக் குறிக்கும்; நீண்ட மேல் திரி விற்பவர்கள் கீழே தள்ளியதைக் குறிக்கும்.",
        "每根K线代表一个周期（这里是一天）。**实体**从开盘价到收盘价；绿色表示收盘高于开盘，"
        "红色表示收盘低于开盘。**影线**显示最高价和最低价。长下影线表示买方把价格推回上方；"
        "长上影线表示卖方把价格压了下来。",
    ),
    "lesson.trend.title": L("Trend", "Trend", "போக்கு", "趋势"),
    "lesson.trend.body": L(
        "An **uptrend** makes higher highs and higher lows. A quick test: price above a rising "
        "50-day and 200-day moving average. Beginners do best trading *with* the trend, not "
        "trying to catch tops and bottoms.",
        "**Trend menaik** membentuk puncak lebih tinggi dan lembah lebih tinggi. Ujian cepat: "
        "harga di atas purata bergerak 50 hari dan 200 hari yang sedang naik. Pemula paling "
        "berjaya bila berdagang *mengikut* trend, bukan cuba meneka puncak dan dasar.",
        "**ஏறுமுகப் போக்கு** உயர்ந்த உச்சங்களையும் உயர்ந்த தாழ்வுகளையும் உருவாக்கும். விரைவுச் "
        "சோதனை: உயரும் 50-நாள் மற்றும் 200-நாள் நகரும் சராசரிக்கு மேல் விலை. தொடக்கநிலையாளர்கள் "
        "உச்சங்களையும் அடிகளையும் பிடிக்க முயலாமல், போக்கு *வழியே* வர்த்தகம் செய்வது சிறந்தது.",
        "**上升趋势**会形成更高的高点和更高的低点。快速判断：价格位于上升中的50日和200日"
        "均线之上。新手最好*顺势*交易，而不是去抄底摸顶。",
    ),
    "lesson.sr.title": L(
        "Support and resistance", "Sokongan dan rintangan", "ஆதரவு மற்றும் எதிர்ப்பு", "支撑与阻力"
    ),
    "lesson.sr.body": L(
        "**Support** is a price area where buying has stopped declines before; **resistance** is "
        "where selling has stopped rallies. These areas are natural places for entries and stops.",
        "**Sokongan** ialah kawasan harga di mana belian pernah menghentikan penurunan; "
        "**rintangan** ialah kawasan di mana jualan pernah menghentikan kenaikan. Kawasan ini "
        "sesuai untuk titik masuk dan henti rugi.",
        "**ஆதரவு** என்பது முன்பு வாங்குதல் சரிவை நிறுத்திய விலைப் பகுதி; **எதிர்ப்பு** என்பது "
        "விற்பனை ஏற்றத்தை நிறுத்திய பகுதி. இவை நுழைவுகளுக்கும் நிறுத்தங்களுக்கும் இயல்பான இடங்கள்.",
        "**支撑**是过去买盘止住下跌的价格区域；**阻力**是卖盘止住上涨的区域。"
        "这些区域是设置入场点和止损的自然位置。",
    ),
    "lesson.stoploss.title": L(
        "Why a stop-loss is mandatory",
        "Kenapa henti rugi wajib",
        "நிறுத்த இழப்பு ஏன் கட்டாயம்",
        "为什么必须设止损",
    ),
    "lesson.stoploss.body": L(
        "A stop-loss is the price where your idea is proven wrong and you exit. Without one, a "
        "single bad trade can wipe out months of gains. In this app you **cannot** open a demo "
        "trade without a stop.",
        "Henti rugi ialah harga di mana idea anda terbukti salah dan anda keluar. Tanpanya, satu "
        "dagangan buruk boleh menghapuskan keuntungan berbulan-bulan. Dalam aplikasi ini anda "
        "**tidak boleh** membuka dagangan demo tanpa henti rugi.",
        "நிறுத்த இழப்பு என்பது உங்கள் யோசனை தவறு என நிரூபிக்கப்பட்டு நீங்கள் வெளியேறும் விலை. "
        "அது இல்லாமல், ஒரு மோசமான வர்த்தகம் பல மாத லாபத்தை அழித்துவிடும். இந்த செயலியில் நிறுத்தம் "
        "இல்லாமல் டெமோ வர்த்தகத்தைத் **திறக்க முடியாது**.",
        "止损是证明你的判断错误、必须离场的价格。没有止损，一笔糟糕的交易就可能抹掉几个月的"
        "利润。在本应用中，没有止损**无法**开立模拟交易。",
    ),
    "lesson.onepct.title": L("The 1% rule", "Peraturan 1%", "1% விதி", "1% 法则"),
    "lesson.onepct.body": L(
        "Risk a small, fixed slice of your account per trade, e.g. 0.5–1%. With $1,000 and 1% "
        "risk you may lose at most $10 if the stop is hit. Ten losses in a row then cost about "
        "10%, which you can recover from.",
        "Risikokan bahagian kecil yang tetap bagi akaun anda untuk setiap dagangan, contohnya "
        "0.5–1%. Dengan $1,000 dan risiko 1%, kerugian maksimum ialah $10 jika henti rugi kena. "
        "Sepuluh kerugian berturut-turut hanya kira-kira 10%, yang masih boleh dipulihkan.",
        "ஒவ்வொரு வர்த்தகத்திலும் உங்கள் கணக்கின் சிறிய, நிலையான பகுதியை மட்டும் இடருக்கு "
        "உட்படுத்துங்கள், எ.கா. 0.5–1%. $1,000 மற்றும் 1% இடருடன், நிறுத்தம் தொட்டால் அதிகபட்சம் "
        "$10 இழப்பீர்கள். தொடர்ந்து பத்து இழப்புகள் சுமார் 10% மட்டுமே — அதிலிருந்து மீளலாம்.",
        "每笔交易只拿账户中一小部分固定比例去冒险，例如 0.5–1%。账户 $1,000、风险 1% 时，"
        "触发止损最多亏 $10。即使连亏十次也只损失约 10%，仍然可以恢复。",
    ),
    "lesson.rmultiple.title": L("R-multiples", "Gandaan R", "R-மடங்குகள்", "R 倍数"),
    "lesson.rmultiple.body": L(
        "**1R** is the amount you risk (entry − stop). A trade that gains twice the risk is "
        "**+2R**; a stopped-out trade is **−1R**. Measuring in R lets you compare trades of any "
        "size.",
        "**1R** ialah jumlah yang anda risikokan (masuk − henti rugi). Dagangan yang untung dua "
        "kali ganda risiko ialah **+2R**; dagangan yang kena henti rugi ialah **−1R**. Mengukur "
        "dalam R membolehkan anda membandingkan dagangan pelbagai saiz.",
        "**1R** என்பது நீங்கள் இடருக்கு உட்படுத்தும் தொகை (நுழைவு − நிறுத்தம்). இடரின் இருமடங்கு "
        "லாபம் தரும் வர்த்தகம் **+2R**; நிறுத்தத்தில் வெளியேறிய வர்த்தகம் **−1R**. R-இல் அளவிடுவது "
        "எந்த அளவு வர்த்தகங்களையும் ஒப்பிட உதவும்.",
        "**1R** 是你承担的风险金额（入场价 − 止损价）。盈利为风险两倍的交易是 **+2R**；"
        "被止损的交易是 **−1R**。用 R 来衡量，可以比较不同规模的交易。",
    ),
    "lesson.rr.title": L(
        "Reward-to-risk", "Ganjaran berbanding risiko", "வெகுமதி-இடர் விகிதம்", "盈亏比"
    ),
    "lesson.rr.body": L(
        "Aim for targets of at least 2R. With 2R winners you can be right only 40% of the time "
        "and still make money: 0.4 × 2 − 0.6 × 1 = +0.2R per trade.",
        "Sasarkan sekurang-kurangnya 2R. Dengan kemenangan 2R, anda boleh betul hanya 40% masa "
        "dan masih untung: 0.4 × 2 − 0.6 × 1 = +0.2R setiap dagangan.",
        "குறைந்தது 2R இலக்குகளை நோக்குங்கள். 2R வெற்றிகளுடன், 40% நேரம் மட்டுமே சரியாக "
        "இருந்தாலும் லாபம் கிடைக்கும்: 0.4 × 2 − 0.6 × 1 = ஒரு வர்த்தகத்திற்கு +0.2R.",
        "目标至少设为 2R。盈利单为 2R 时，即使胜率只有 40% 也能赚钱："
        "0.4 × 2 − 0.6 × 1 = 每笔 +0.2R。",
    ),
    "lesson.sizing.title": L("Position sizing", "Saiz posisi", "நிலை அளவு", "仓位大小"),
    "lesson.sizing.body": L(
        "Shares = (account × risk %) ÷ (entry − stop). Use the **Position Sizer** page or the "
        "ATR method: stop = entry − 2 × ATR. Small accounts can use fractional shares.",
        "Bilangan saham = (akaun × % risiko) ÷ (masuk − henti rugi). Gunakan halaman "
        "**Kalkulator Saiz Posisi** atau kaedah ATR: henti rugi = masuk − 2 × ATR. Akaun kecil "
        "boleh guna saham pecahan.",
        "பங்குகள் = (கணக்கு × இடர் %) ÷ (நுழைவு − நிறுத்தம்). **நிலை அளவு கணிப்பான்** பக்கத்தை "
        "அல்லது ATR முறையைப் பயன்படுத்துங்கள்: நிறுத்தம் = நுழைவு − 2 × ATR. சிறிய கணக்குகள் "
        "பகுதிப் பங்குகளைப் பயன்படுத்தலாம்.",
        "股数 =（账户 × 风险%）÷（入场价 − 止损价）。可使用**仓位计算器**页面，或 ATR 方法："
        "止损 = 入场价 − 2 × ATR。小账户可以使用零碎股。",
    ),
    "lesson.breadth.title": L("Market breadth", "Keluasan pasaran", "சந்தை அகலம்", "市场广度"),
    "lesson.breadth.body": L(
        "Most stocks follow the overall market. Check **Market Breadth** before trading: a weak "
        "score means smaller size or fewer trades.",
        "Kebanyakan saham mengikut pasaran keseluruhan. Semak **Keluasan Pasaran** sebelum "
        "berdagang: skor lemah bermaksud saiz lebih kecil atau kurangkan dagangan.",
        "பெரும்பாலான பங்குகள் ஒட்டுமொத்த சந்தையைப் பின்பற்றும். வர்த்தகத்திற்கு முன் **சந்தை "
        "அகலம்** பார்க்கவும்: பலவீனமான மதிப்பெண் என்றால் சிறிய அளவு அல்லது குறைவான வர்த்தகங்கள்.",
        "大多数股票跟随大盘。交易前先看**市场广度**：评分偏弱时应缩小仓位或减少交易。",
    ),
    "lesson.rsi_atr.title": L("RSI and ATR", "RSI dan ATR", "RSI மற்றும் ATR", "RSI 与 ATR"),
    "lesson.rsi_atr.body": L(
        "**RSI** above 70 is stretched, below 30 is washed out; in uptrends, pullbacks to 40–50 "
        "are often better entries than chasing above 70. **ATR** measures normal daily movement; "
        "a stop tighter than ~1 ATR is often hit by noise.",
        "**RSI** melebihi 70 bermaksud terlebih regang, bawah 30 terlebih jual; dalam trend "
        "menaik, anjakan balik ke 40–50 selalunya titik masuk lebih baik daripada mengejar di "
        "atas 70. **ATR** mengukur pergerakan harian biasa; henti rugi lebih ketat daripada ~1 "
        "ATR sering terkena oleh gangguan harga.",
        "**RSI** 70க்கு மேல் என்றால் அதிகமாக நீண்டுள்ளது, 30க்குக் கீழ் என்றால் அதிகமாக "
        "விற்கப்பட்டுள்ளது; ஏறுமுகப் போக்கில், 70க்கு மேல் துரத்துவதை விட 40–50க்கு இறங்குவது "
        "சிறந்த நுழைவு. **ATR** சாதாரண தினசரி அசைவை அளவிடும்; ~1 ATR-ஐ விட நெருக்கமான நிறுத்தம் "
        "பெரும்பாலும் சத்தத்தால் தொடப்படும்.",
        "**RSI** 高于 70 表示过度延伸，低于 30 表示超卖；在上升趋势中，回调到 40–50 往往比在 "
        "70 以上追高更好。**ATR** 衡量正常的日波动；止损小于约 1 个 ATR 时，常被正常波动扫掉。",
    ),
    "lesson.expectancy.title": L("Expectancy", "Jangkaan", "எதிர்பார்ப்பு", "期望值"),
    "lesson.expectancy.body": L(
        "Expectancy = average R per trade. It matters more than win rate. Keep a journal (the "
        "demo account does this for you) and review your losers.",
        "Jangkaan = purata R setiap dagangan. Ia lebih penting daripada kadar menang. Simpan "
        "jurnal (akaun demo melakukannya untuk anda) dan kaji dagangan yang rugi.",
        "எதிர்பார்ப்பு = ஒரு வர்த்தகத்திற்கான சராசரி R. இது வெற்றி விகிதத்தை விட முக்கியம். "
        "நாட்குறிப்பை வைத்திருங்கள் (டெமோ கணக்கு இதைச் செய்யும்) மற்றும் இழப்புகளை ஆய்வு செய்யுங்கள்.",
        "期望值 = 每笔交易的平均 R，它比胜率更重要。坚持写交易日志（模拟账户会自动记录），"
        "并复盘亏损的交易。",
    ),
    "lesson.setups.title": L("Setups", "Setup dagangan", "வர்த்தக அமைப்புகள்", "交易形态"),
    "lesson.setups.body": L(
        "Explore the **Skill Catalog**: VCP Screener, Breakout Trade Planner, PEAD Screener, "
        "CANSLIM and others encode specific, testable entry rules.",
        "Terokai **Katalog Skill**: VCP Screener, Breakout Trade Planner, PEAD Screener, CANSLIM "
        "dan lain-lain mengandungi peraturan kemasukan khusus yang boleh diuji.",
        "**திறன் பட்டியலை** ஆராயுங்கள்: VCP Screener, Breakout Trade Planner, PEAD Screener, "
        "CANSLIM போன்றவை குறிப்பிட்ட, சோதிக்கக்கூடிய நுழைவு விதிகளைக் கொண்டுள்ளன.",
        "浏览**技能目录**：VCP Screener、Breakout Trade Planner、PEAD Screener、CANSLIM "
        "等都包含具体、可检验的入场规则。",
    ),
    "lesson.process.title": L(
        "Process over outcome",
        "Proses lebih penting daripada hasil",
        "முடிவை விட செயல்முறை முக்கியம்",
        "重过程，轻结果",
    ),
    "lesson.process.body": L(
        "Write a rule set, test it (Chart Replay, Backtest Expert), then trade it small. Change "
        "one thing at a time and judge it over 20+ trades, not one.",
        "Tulis set peraturan, uji (Ulang Tayang Carta, Backtest Expert), kemudian dagangkan "
        "dengan saiz kecil. Ubah satu perkara pada satu masa dan nilai selepas 20+ dagangan, "
        "bukan satu.",
        "விதிகளை எழுதுங்கள், சோதியுங்கள் (விளக்கப்பட மறுஇயக்கம், Backtest Expert), பின் சிறிய "
        "அளவில் வர்த்தகம் செய்யுங்கள். ஒரே நேரத்தில் ஒன்றை மட்டும் மாற்றி, ஒன்றல்ல 20+ "
        "வர்த்தகங்களில் மதிப்பிடுங்கள்.",
        "写下规则，加以测试（图表回放、Backtest Expert），再用小仓位实盘。每次只改一项，"
        "并以 20 笔以上而不是一笔交易来评判。",
    ),
    # ------------------------------------------------------------------ quiz
    "quiz.1.q": L(
        "A green candle means…", "Lilin hijau bermaksud…", "பச்சை மெழுகுவர்த்தி என்றால்…", "绿色K线表示……"
    ),
    "quiz.1.opts": L(
        ["Close above open", "Close below open", "High volume", "Price gapped up"],
        ["Tutup di atas buka", "Tutup di bawah buka", "Volum tinggi", "Harga melompat naik"],
        ["முடிவு திறப்புக்கு மேல்", "முடிவு திறப்புக்குக் கீழ்", "அதிக அளவு", "விலை இடைவெளியுடன் உயர்ந்தது"],
        ["收盘高于开盘", "收盘低于开盘", "成交量大", "价格跳空高开"],
    ),
    "quiz.2.q": L(
        "An uptrend is best described as…",
        "Trend menaik paling tepat digambarkan sebagai…",
        "ஏறுமுகப் போக்கை சிறப்பாக விவரிப்பது…",
        "上升趋势最准确的描述是……",
    ),
    "quiz.2.opts": L(
        [
            "Lower highs and lower lows",
            "Higher highs and higher lows",
            "Price stuck in a range",
            "RSI above 70",
        ],
        [
            "Puncak dan lembah makin rendah",
            "Puncak dan lembah makin tinggi",
            "Harga tersekat dalam julat",
            "RSI melebihi 70",
        ],
        [
            "தாழ்ந்த உச்சங்கள், தாழ்ந்த தாழ்வுகள்",
            "உயர்ந்த உச்சங்கள், உயர்ந்த தாழ்வுகள்",
            "விலை ஒரு வரம்பில் சிக்கியுள்ளது",
            "RSI 70க்கு மேல்",
        ],
        ["高点和低点不断降低", "高点和低点不断抬高", "价格在区间内横盘", "RSI 高于 70"],
    ),
    "quiz.3.q": L(
        "Account $1,000, risk 1%, entry $50, stop $48. How many shares?",
        "Akaun $1,000, risiko 1%, masuk $50, henti rugi $48. Berapa saham?",
        "கணக்கு $1,000, இடர் 1%, நுழைவு $50, நிறுத்தம் $48. எத்தனை பங்குகள்?",
        "账户 $1,000，风险 1%，入场 $50，止损 $48。应买多少股？",
    ),
    "quiz.3.opts": L(
        ["2", "20", "5", "10"],
        ["2", "20", "5", "10"],
        ["2", "20", "5", "10"],
        ["2", "20", "5", "10"],
    ),
    "quiz.4.q": L(
        "When should you decide on your stop-loss?",
        "Bilakah anda patut tentukan henti rugi?",
        "நிறுத்த இழப்பை எப்போது முடிவு செய்ய வேண்டும்?",
        "什么时候应该确定止损？",
    ),
    "quiz.4.opts": L(
        [
            "After the trade goes against you",
            "Never; just hold",
            "When the news changes",
            "Before you enter the trade",
        ],
        [
            "Selepas dagangan bergerak melawan anda",
            "Tidak perlu; simpan sahaja",
            "Apabila berita berubah",
            "Sebelum anda masuk dagangan",
        ],
        [
            "வர்த்தகம் உங்களுக்கு எதிராகச் சென்ற பிறகு",
            "ஒருபோதும் இல்லை; வைத்திருங்கள்",
            "செய்தி மாறும்போது",
            "வர்த்தகத்தில் நுழைவதற்கு முன்",
        ],
        ["交易对你不利之后", "不用设，一直持有", "消息面变化时", "入场之前"],
    ),
    "quiz.5.q": L(
        "Entry $100, stop $95, exit $110. The result is…",
        "Masuk $100, henti rugi $95, keluar $110. Hasilnya…",
        "நுழைவு $100, நிறுத்தம் $95, வெளியேற்றம் $110. முடிவு…",
        "入场 $100，止损 $95，出场 $110。结果是……",
    ),
    "quiz.5.opts": L(
        ["+2R", "+1R", "+10R", "−1R"],
        ["+2R", "+1R", "+10R", "−1R"],
        ["+2R", "+1R", "+10R", "−1R"],
        ["+2R", "+1R", "+10R", "−1R"],
    ),
    # ------------------------------------------------------------------ learn page
    "learn.intro": L(
        "Each level unlocks by doing, not by reading: pass the quiz, practise on historical "
        "charts, then prove it on the demo account.",
        "Setiap tahap dibuka dengan melakukan, bukan membaca: lulus kuiz, berlatih pada carta "
        "sejarah, kemudian buktikan dalam akaun demo.",
        "ஒவ்வொரு நிலையும் படிப்பதால் அல்ல, செய்வதால் திறக்கும்: வினாடி வினாவில் தேர்ச்சி, "
        "வரலாற்று விளக்கப்படங்களில் பயிற்சி, பின் டெமோ கணக்கில் நிரூபியுங்கள்.",
        "每个级别要靠实践解锁，而不是阅读：通过测验，在历史图表上练习，再在模拟账户中证明自己。",
    ),
    "learn.max_risk": L(
        "Max risk/trade: **{pct}%**",
        "Risiko maks/dagangan: **{pct}%**",
        "அதிகபட்ச இடர்/வர்த்தகம்: **{pct}%**",
        "单笔最大风险：**{pct}%**",
    ),
    "learn.progress": L("Your progress", "Kemajuan anda", "உங்கள் முன்னேற்றம்", "你的进度"),
    "learn.m_quiz": L("Quiz", "Kuiz", "வினாடி வினா", "测验"),
    "learn.passed": L("passed", "lulus", "தேர்ச்சி", "已通过"),
    "learn.not_passed": L("not passed", "belum lulus", "தேர்ச்சி இல்லை", "未通过"),
    "learn.m_replays": L("Replay trades", "Dagangan ulang tayang", "மறுஇயக்க வர்த்தகங்கள்", "回放交易"),
    "learn.avg_r": L("{r}R avg", "purata {r}R", "சராசரி {r}R", "平均 {r}R"),
    "learn.m_demo": L(
        "Demo trades closed", "Dagangan demo ditutup", "மூடப்பட்ட டெமோ வர்த்தகங்கள்", "已平仓模拟交易"
    ),
    "learn.m_expect": L("Demo expectancy", "Jangkaan demo", "டெமோ எதிர்பார்ப்பு", "模拟期望值"),
    "learn.next": L(
        "**Next step:** {unlock}",
        "**Langkah seterusnya:** {unlock}",
        "**அடுத்த படி:** {unlock}",
        "**下一步：**{unlock}",
    ),
    "learn.top": L(
        "You've reached the top level. Keep journaling and reviewing.",
        "Anda sudah di tahap tertinggi. Teruskan menulis jurnal dan membuat semakan.",
        "நீங்கள் உயர்ந்த நிலையை அடைந்துவிட்டீர்கள். நாட்குறிப்பு எழுதுவதையும் மதிப்பாய்வையும் தொடருங்கள்.",
        "你已达到最高级别。继续写日志并坚持复盘。",
    ),
    "learn.lessons": L(
        "Level {n} lessons: {name}",
        "Pelajaran Tahap {n}: {name}",
        "நிலை {n} பாடங்கள்: {name}",
        "第 {n} 级课程：{name}",
    ),
    "learn.review": L(
        "Review earlier levels",
        "Ulang kaji tahap sebelumnya",
        "முந்தைய நிலைகளை மீளாய்வு செய்யுங்கள்",
        "复习之前的级别",
    ),
    "learn.quiz": L("Basics quiz", "Kuiz asas", "அடிப்படை வினாடி வினா", "基础测验"),
    "learn.submit": L("Submit answers", "Hantar jawapan", "பதில்களைச் சமர்ப்பிக்கவும்", "提交答案"),
    "learn.quiz_pass": L(
        "{score}/{total} — passed! Level 2 unlocked.",
        "{score}/{total} — lulus! Tahap 2 dibuka.",
        "{score}/{total} — தேர்ச்சி! நிலை 2 திறக்கப்பட்டது.",
        "{score}/{total} — 通过！已解锁第 2 级。",
    ),
    "learn.quiz_fail": L(
        "{score}/{total} — review the lessons and try again.",
        "{score}/{total} — ulang kaji pelajaran dan cuba lagi.",
        "{score}/{total} — பாடங்களை மீண்டும் படித்து மீண்டும் முயற்சிக்கவும்.",
        "{score}/{total} — 请复习课程后再试一次。",
    ),
    "learn.btn_replay": L(
        "▶ Practise on Chart Replay",
        "▶ Berlatih di Ulang Tayang Carta",
        "▶ விளக்கப்பட மறுஇயக்கத்தில் பயிற்சி",
        "▶ 去图表回放练习",
    ),
    "learn.btn_demo": L(
        "💼 Open Demo Account", "💼 Buka Akaun Demo", "💼 டெமோ கணக்கைத் திறக்கவும்", "💼 打开模拟账户"
    ),
    # ------------------------------------------------------------------ replay page
    "replay.intro": L(
        "A random stock is shown up to a hidden point in the past. Decide: buy with a stop and "
        "target, or skip. Then the next {h} days are revealed. Ticker and dates are hidden so "
        "you judge the chart, not the name.",
        "Saham rawak ditunjukkan sehingga satu titik tersembunyi pada masa lalu. Buat keputusan: "
        "beli dengan henti rugi dan sasaran, atau langkau. Kemudian {h} hari seterusnya "
        "didedahkan. Nama saham dan tarikh disembunyikan supaya anda menilai carta, bukan nama.",
        "ஒரு சீரற்ற பங்கு கடந்த காலத்தின் மறைக்கப்பட்ட புள்ளி வரை காட்டப்படும். முடிவு செய்யுங்கள்: "
        "நிறுத்தம் மற்றும் இலக்குடன் வாங்கவும், அல்லது தவிர்க்கவும். பின் அடுத்த {h} நாட்கள் "
        "வெளிப்படுத்தப்படும். பெயரை அல்ல, விளக்கப்படத்தை மதிப்பிட குறியீடும் தேதிகளும் மறைக்கப்படும்.",
        "系统随机显示一只股票截至过去某个隐藏时点的走势。请决定：设好止损和目标后买入，或者跳过。"
        "随后揭晓接下来 {h} 天的走势。股票代码和日期都被隐藏，让你只看图表、不看名字。",
    ),
    "replay.m_trades": L("Replay trades", "Dagangan ulang tayang", "மறுஇயக்க வர்த்தகங்கள்", "回放交易"),
    "replay.m_total": L("Total", "Jumlah", "மொத்தம்", "合计"),
    "replay.caption": L(
        "Last close **{close}** · ATR(14) **{atr}** · RSI(14) **{rsi}**",
        "Harga tutup terakhir **{close}** · ATR(14) **{atr}** · RSI(14) **{rsi}**",
        "கடைசி முடிவு விலை **{close}** · ATR(14) **{atr}** · RSI(14) **{rsi}**",
        "最新收盘价 **{close}** · ATR(14) **{atr}** · RSI(14) **{rsi}**",
    ),
    "replay.reason": L(
        "Why this trade? (one line)",
        "Kenapa dagangan ini? (satu baris)",
        "ஏன் இந்த வர்த்தகம்? (ஒரு வரி)",
        "为什么做这笔交易？（一句话）",
    ),
    "replay.rr": L(
        "Risk {risk} · reward {reward} · R:R = {rr}",
        "Risiko {risk} · ganjaran {reward} · R:R = {rr}",
        "இடர் {risk} · வெகுமதி {reward} · R:R = {rr}",
        "风险 {risk} · 回报 {reward} · 盈亏比 = {rr}",
    ),
    "replay.buy": L(
        "🟢 Buy at last close",
        "🟢 Beli pada harga tutup terakhir",
        "🟢 கடைசி முடிவு விலையில் வாங்கவும்",
        "🟢 以最新收盘价买入",
    ),
    "replay.skip": L(
        "⏭ Skip — no trade", "⏭ Langkau — tiada dagangan", "⏭ தவிர் — வர்த்தகம் இல்லை", "⏭ 跳过——不交易"
    ),
    "replay.skipped": L(
        "You skipped. Over the next {h} days price moved {move}. ({reveal})",
        "Anda melangkau. Dalam {h} hari seterusnya harga bergerak {move}. ({reveal})",
        "நீங்கள் தவிர்த்தீர்கள். அடுத்த {h} நாட்களில் விலை {move} நகர்ந்தது. ({reveal})",
        "你选择了跳过。接下来 {h} 天价格变动 {move}。（{reveal}）",
    ),
    "replay.target_hit": L(
        "🎯 Target hit", "🎯 Sasaran tercapai", "🎯 இலக்கு எட்டப்பட்டது", "🎯 达到目标"
    ),
    "replay.stopped": L(
        "🛑 Stopped out", "🛑 Kena henti rugi", "🛑 நிறுத்தத்தில் வெளியேறியது", "🛑 触发止损"
    ),
    "replay.time": L(
        "⏱ Neither hit in {h} days — exited at close",
        "⏱ Tiada yang kena dalam {h} hari — keluar pada harga tutup",
        "⏱ {h} நாட்களில் எதுவும் தொடப்படவில்லை — முடிவு விலையில் வெளியேறியது",
        "⏱ {h} 天内均未触及——按收盘价离场",
    ),
    "replay.result": L(
        "{msg} after {bars} bars at {price} → **{r}R**. ({reveal})",
        "{msg} selepas {bars} bar pada {price} → **{r}R**. ({reveal})",
        "{bars} பார்களுக்குப் பிறகு {price} இல் {msg} → **{r}R**. ({reveal})",
        "{msg}，经过 {bars} 根K线，价格 {price} → **{r}R**。（{reveal}）",
    ),
    "replay.tip_tight": L(
        "Tip: your stop was tighter than 1 ATR, so normal daily noise can hit it.",
        "Petua: henti rugi anda lebih ketat daripada 1 ATR, jadi gangguan harian biasa boleh "
        "mengenainya.",
        "குறிப்பு: உங்கள் நிறுத்தம் 1 ATR-ஐ விட நெருக்கமாக இருந்தது; சாதாரண தினசரி அசைவு அதைத் தொடலாம்.",
        "提示：你的止损小于 1 个 ATR，正常的日内波动就可能触发它。",
    ),
    "replay.next": L("Next chart ▶", "Carta seterusnya ▶", "அடுத்த விளக்கப்படம் ▶", "下一张图 ▶"),
    "replay.more": L(
        "{n} more replay trades to reach Level 3.",
        "{n} lagi dagangan ulang tayang untuk ke Tahap 3.",
        "நிலை 3 ஐ அடைய இன்னும் {n} மறுஇயக்க வர்த்தகங்கள்.",
        "再完成 {n} 笔回放交易即可升到第 3 级。",
    ),
    "replay.hidden": L(
        "hidden future", "masa depan tersembunyi", "மறைக்கப்பட்ட எதிர்காலம்", "隐藏的未来"
    ),
    "replay.axis": L(
        "bars (dates hidden)",
        "bar (tarikh disembunyikan)",
        "பார்கள் (தேதிகள் மறைக்கப்பட்டன)",
        "K线（日期已隐藏）",
    ),
    # ------------------------------------------------------------------ demo page
    "demo.caption": L(
        "Level {n} · {name} — max risk per trade **{pct}%**. Long trades only. Every trade "
        "needs a stop-loss and a reason. Fractional shares allowed.",
        "Tahap {n} · {name} — risiko maks setiap dagangan **{pct}%**. Beli (long) sahaja. Setiap "
        "dagangan perlu henti rugi dan sebab. Saham pecahan dibenarkan.",
        "நிலை {n} · {name} — ஒரு வர்த்தகத்திற்கு அதிகபட்ச இடர் **{pct}%**. வாங்கும் (long) "
        "வர்த்தகங்கள் மட்டும். ஒவ்வொரு வர்த்தகத்திற்கும் நிறுத்த இழப்பும் காரணமும் தேவை. "
        "பகுதிப் பங்குகள் அனுமதிக்கப்படும்.",
        "第 {n} 级 · {name} — 单笔最大风险 **{pct}%**。仅限做多。每笔交易都需要止损和理由。"
        "允许零碎股。",
    ),
    "demo.setup": L(
        "Start a paper-trading account with virtual money. Prices are real daily closes.",
        "Mulakan akaun dagangan kertas dengan wang maya. Harga ialah harga tutup harian sebenar.",
        "மெய்நிகர் பணத்துடன் காகித வர்த்தகக் கணக்கைத் தொடங்குங்கள். விலைகள் உண்மையான தினசரி முடிவு விலைகள்.",
        "用虚拟资金开设模拟交易账户。价格为真实的每日收盘价。",
    ),
    "demo.type": L("Account type", "Jenis akaun", "கணக்கு வகை", "账户类型"),
    "demo.type.standard": L(
        "Standard (USD): $100 – $1,000",
        "Standard (USD): $100 – $1,000",
        "நிலையான (USD): $100 – $1,000",
        "标准账户 (USD)：$100 – $1,000",
    ),
    "demo.type.cent": L(
        "Cent (USC): 10,000 – 1,000,000 cents",
        "Cent (USC): 10,000 – 1,000,000 sen",
        "சென்ட் (USC): 10,000 – 1,000,000 சென்ட்கள்",
        "美分账户 (USC)：10,000 – 1,000,000 美分",
    ),
    "demo.cent_help": L(
        "1 USD = 100 US cents (USC). A cent account shows balances in cents: 100,000 USC = $1,000.",
        "1 USD = 100 sen AS (USC). Akaun cent memaparkan baki dalam sen: 100,000 USC = $1,000.",
        "1 USD = 100 அமெரிக்க சென்ட்கள் (USC). சென்ட் கணக்கு இருப்பை சென்ட்களில் காட்டும்: 100,000 USC = $1,000.",
        "1 美元 = 100 美分 (USC)。美分账户以美分显示余额：100,000 USC = $1,000。",
    ),
    "demo.balance": L("Starting balance", "Baki permulaan", "தொடக்க இருப்பு", "初始资金"),
    "demo.create": L(
        "Create demo account", "Cipta akaun demo", "டெமோ கணக்கை உருவாக்கவும்", "创建模拟账户"
    ),
    "demo.acct": L(
        "Account: **{type}** · started with {start}",
        "Akaun: **{type}** · bermula dengan {start}",
        "கணக்கு: **{type}** · தொடக்கம் {start}",
        "账户：**{type}** · 初始资金 {start}",
    ),
    "demo.m_equity": L("Equity", "Ekuiti", "ஈக்விட்டி", "净值"),
    "demo.m_cash": L("Cash", "Tunai", "ரொக்கம்", "现金"),
    "demo.m_closed": L("Closed trades", "Dagangan ditutup", "மூடப்பட்ட வர்த்தகங்கள்", "已平仓交易"),
    "demo.tab_new": L("New trade", "Dagangan baru", "புதிய வர்த்தகம்", "新交易"),
    "demo.tab_open": L("Open ({n})", "Terbuka ({n})", "திறந்தவை ({n})", "持仓 ({n})"),
    "demo.tab_journal": L("Journal ({n})", "Jurnal ({n})", "நாட்குறிப்பு ({n})", "日志 ({n})"),
    "demo.reset_title": L("Reset account", "Set semula akaun", "கணக்கை மீட்டமைக்கவும்", "重置账户"),
    "demo.reset_warn": L(
        "This deletes all demo trades and history. You can then choose a new account type.",
        "Ini memadam semua dagangan demo dan sejarah. Anda boleh pilih jenis akaun baharu.",
        "இது அனைத்து டெமோ வர்த்தகங்களையும் வரலாற்றையும் நீக்கும். பின் புதிய கணக்கு வகையைத் தேர்வு செய்யலாம்.",
        "这将删除所有模拟交易和历史记录，之后可以重新选择账户类型。",
    ),
    "demo.reset_btn": L(
        "Reset demo account", "Set semula akaun demo", "டெமோ கணக்கை மீட்டமைக்கவும்", "重置模拟账户"
    ),
    "demo.placeholder": L("e.g. AAPL", "cth. AAPL", "எ.கா. AAPL", "例如 AAPL"),
    "demo.quote": L("Get quote", "Dapatkan harga", "விலையைப் பெறவும்", "获取报价"),
    "demo.quote_line": L(
        "**{sym}** last close **{close}** ({date}) · ATR {atr} · RSI {rsi} · trend: {trend}",
        "**{sym}** harga tutup terakhir **{close}** ({date}) · ATR {atr} · RSI {rsi} · trend: "
        "{trend}",
        "**{sym}** கடைசி முடிவு விலை **{close}** ({date}) · ATR {atr} · RSI {rsi} · போக்கு: {trend}",
        "**{sym}** 最新收盘价 **{close}**（{date}）· ATR {atr} · RSI {rsi} · 趋势：{trend}",
    ),
    "demo.trend_up": L(
        "🟢 up (above 50 & 200 SMA)",
        "🟢 naik (atas SMA 50 & 200)",
        "🟢 ஏறுமுகம் (50 & 200 SMA க்கு மேல்)",
        "🟢 上升（高于 50 和 200 日均线）",
    ),
    "demo.trend_no": L(
        "🟠 not a clean uptrend",
        "🟠 bukan trend menaik yang jelas",
        "🟠 தெளிவான ஏறுமுகம் இல்லை",
        "🟠 并非明确的上升趋势",
    ),
    "demo.shares": L("Shares", "Bilangan saham", "பங்குகள்", "股数"),
    "demo.shares_help": L(
        "Default = most shares allowed by your {pct}% risk limit and your cash.",
        "Lalai = bilangan saham maksimum yang dibenarkan oleh had risiko {pct}% dan tunai anda.",
        "இயல்புநிலை = உங்கள் {pct}% இடர் வரம்பும் ரொக்கமும் அனுமதிக்கும் அதிகபட்ச பங்குகள்.",
        "默认值 = 在 {pct}% 风险上限和现金允许范围内的最大股数。",
    ),
    "demo.risk_preview": L(
        "Cost {cost} · risk {risk} ({pct}% of equity)",
        "Kos {cost} · risiko {risk} ({pct}% daripada ekuiti)",
        "செலவு {cost} · இடர் {risk} (ஈக்விட்டியின் {pct}%)",
        "成本 {cost} · 风险 {risk}（占净值 {pct}%）",
    ),
    "demo.reason": L(
        "Why are you taking this trade? (required)",
        "Kenapa anda ambil dagangan ini? (wajib)",
        "இந்த வர்த்தகத்தை ஏன் எடுக்கிறீர்கள்? (கட்டாயம்)",
        "你为什么做这笔交易？（必填）",
    ),
    "demo.checklist": L(
        "**Pre-trade checklist**",
        "**Senarai semak sebelum dagangan**",
        "**வர்த்தகத்திற்கு முந்தைய சரிபார்ப்பு**",
        "**交易前检查清单**",
    ),
    "demo.chk1": L(
        "I know where I'm wrong (stop) before entering",
        "Saya tahu di mana saya salah (henti rugi) sebelum masuk",
        "நுழைவதற்கு முன் நான் எங்கே தவறு என்பதை (நிறுத்தம்) அறிவேன்",
        "入场前我清楚在哪里认错（止损）",
    ),
    "demo.chk2": L(
        "The reward is at least 2× the risk",
        "Ganjaran sekurang-kurangnya 2× risiko",
        "வெகுமதி இடரின் குறைந்தது 2 மடங்கு",
        "潜在回报至少是风险的 2 倍",
    ),
    "demo.chk3": L(
        "I checked the overall market (Market Breadth)",
        "Saya sudah semak pasaran keseluruhan (Keluasan Pasaran)",
        "ஒட்டுமொத்த சந்தையைச் சரிபார்த்தேன் (சந்தை அகலம்)",
        "我已检查大盘（市场广度）",
    ),
    "demo.buy": L(
        "Buy at last close",
        "Beli pada harga tutup terakhir",
        "கடைசி முடிவு விலையில் வாங்கவும்",
        "以最新收盘价买入",
    ),
    "demo.err_reason": L(
        "Write a reason first — it goes into your journal.",
        "Tulis sebab dahulu — ia akan masuk ke jurnal anda.",
        "முதலில் காரணத்தை எழுதுங்கள் — அது உங்கள் நாட்குறிப்பில் சேரும்.",
        "请先写下理由——它会记入你的交易日志。",
    ),
    "demo.err_check": L(
        "Tick every checklist item first.",
        "Tandakan semua item senarai semak dahulu.",
        "முதலில் அனைத்து சரிபார்ப்பு உருப்படிகளையும் குறிக்கவும்.",
        "请先勾选所有检查项。",
    ),
    "demo.bought": L(
        "Bought {shares} {sym} at {price}. Risk {risk} ({pct}%).",
        "Membeli {shares} {sym} pada {price}. Risiko {risk} ({pct}%).",
        "{sym} இன் {shares} பங்குகள் {price} இல் வாங்கப்பட்டன. இடர் {risk} ({pct}%).",
        "已以 {price} 买入 {shares} 股 {sym}。风险 {risk}（{pct}%）。",
    ),
    "demo.err.shares": L(
        "Shares must be more than zero.",
        "Bilangan saham mesti lebih daripada sifar.",
        "பங்குகள் பூஜ்ஜியத்தை விட அதிகமாக இருக்க வேண்டும்.",
        "股数必须大于零。",
    ),
    "demo.err.stop": L(
        "A stop-loss below the entry price is required.",
        "Henti rugi di bawah harga masuk diperlukan.",
        "நுழைவு விலைக்குக் கீழே நிறுத்த இழப்பு தேவை.",
        "必须设置低于入场价的止损。",
    ),
    "demo.err.target": L(
        "Target must be above the entry price.",
        "Sasaran mesti di atas harga masuk.",
        "இலக்கு நுழைவு விலைக்கு மேல் இருக்க வேண்டும்.",
        "目标价必须高于入场价。",
    ),
    "demo.err.cash": L(
        "Not enough cash: need {need}, have {have}.",
        "Tunai tidak mencukupi: perlu {need}, ada {have}.",
        "போதுமான ரொக்கம் இல்லை: தேவை {need}, உள்ளது {have}.",
        "现金不足：需要 {need}，可用 {have}。",
    ),
    "demo.err.risk": L(
        "Trade risk {pct}% exceeds your level's limit of {limit}%. Reduce shares or tighten "
        "the stop.",
        "Risiko dagangan {pct}% melebihi had tahap anda {limit}%. Kurangkan saham atau ketatkan "
        "henti rugi.",
        "வர்த்தக இடர் {pct}% உங்கள் நிலையின் {limit}% வரம்பை மீறுகிறது. பங்குகளைக் குறைக்கவும் "
        "அல்லது நிறுத்தத்தை நெருக்கவும்.",
        "该交易风险 {pct}% 超过你当前级别 {limit}% 的上限。请减少股数或收紧止损。",
    ),
    "demo.toast": L(
        "{sym}: {reason} at {price} ({r}R)",
        "{sym}: {reason} pada {price} ({r}R)",
        "{sym}: {price} இல் {reason} ({r}R)",
        "{sym}：{reason}，价格 {price}（{r}R）",
    ),
    "demo.reason.stop": L("stop-loss hit", "henti rugi kena", "நிறுத்தம் தொடப்பட்டது", "触发止损"),
    "demo.reason.target": L("target hit", "sasaran tercapai", "இலக்கு எட்டப்பட்டது", "达到目标"),
    "demo.reason.manual": L("closed manually", "ditutup manual", "கைமுறையாக மூடப்பட்டது", "手动平仓"),
    "demo.no_open": L(
        "No open positions.", "Tiada posisi terbuka.", "திறந்த நிலைகள் இல்லை.", "暂无持仓。"
    ),
    "demo.open_caption": L(
        "Stops and targets are checked against each new daily bar when this page loads.",
        "Henti rugi dan sasaran disemak terhadap setiap bar harian baharu apabila halaman ini "
        "dimuatkan.",
        "இந்தப் பக்கம் ஏற்றப்படும்போது ஒவ்வொரு புதிய தினசரி பாருக்கும் நிறுத்தங்களும் இலக்குகளும் சரிபார்க்கப்படும்.",
        "每次打开本页时，系统会用最新的日K线检查止损和目标。",
    ),
    "demo.pos_entry": L(
        "Entry {entry}  \nNow **{now}**",
        "Masuk {entry}  \nKini **{now}**",
        "நுழைவு {entry}  \nதற்போது **{now}**",
        "入场 {entry}  \n现价 **{now}**",
    ),
    "demo.pos_levels": L(
        "Stop {stop}  \nTarget {target}",
        "Henti rugi {stop}  \nSasaran {target}",
        "நிறுத்தம் {stop}  \nஇலக்கு {target}",
        "止损 {stop}  \n目标 {target}",
    ),
    "demo.pos_pnl": L(
        "P&L **{pnl}**  \n{r}R",
        "Untung/Rugi **{pnl}**  \n{r}R",
        "லாபம்/நட்டம் **{pnl}**  \n{r}R",
        "盈亏 **{pnl}**  \n{r}R",
    ),
    "demo.close": L("Close", "Tutup", "மூடு", "平仓"),
    "demo.note": L("Reason: {note}", "Sebab: {note}", "காரணம்: {note}", "理由：{note}"),
    "demo.no_closed": L(
        "Closed trades appear here.",
        "Dagangan yang ditutup akan dipaparkan di sini.",
        "மூடப்பட்ட வர்த்தகங்கள் இங்கே தோன்றும்.",
        "已平仓的交易会显示在这里。",
    ),
    "demo.axis_trade": L("trade #", "dagangan #", "வர்த்தகம் #", "交易 #"),
    "demo.axis_account": L("account", "akaun", "கணக்கு", "账户"),
    "demo.worst": L(
        "Your worst trade ({sym}) lost {r}R — more than your planned risk. That usually means a "
        "gap or a moved stop.",
        "Dagangan terburuk anda ({sym}) rugi {r}R — lebih daripada risiko yang dirancang. "
        "Biasanya ini disebabkan harga melompat (gap) atau henti rugi dialihkan.",
        "உங்கள் மோசமான வர்த்தகம் ({sym}) {r}R இழந்தது — திட்டமிட்ட இடரை விட அதிகம். இது "
        "பொதுவாக விலை இடைவெளி அல்லது நகர்த்தப்பட்ட நிறுத்தத்தால் ஏற்படும்.",
        "你最差的一笔交易（{sym}）亏损 {r}R，超过了计划风险。通常是跳空或移动了止损所致。",
    ),
    "col.symbol": L("Symbol", "Simbol", "குறியீடு", "代码"),
    "col.entry_date": L("Entry date", "Tarikh masuk", "நுழைவு தேதி", "入场日期"),
    "col.exit_date": L("Exit date", "Tarikh keluar", "வெளியேறும் தேதி", "出场日期"),
    "col.entry": L("Entry", "Masuk", "நுழைவு", "入场价"),
    "col.exit_price": L("Exit", "Keluar", "வெளியேற்றம்", "出场价"),
    "col.stop": L("Stop", "Henti rugi", "நிறுத்தம்", "止损"),
    "col.shares": L("Shares", "Saham", "பங்குகள்", "股数"),
    "col.exit_reason": L("Exit reason", "Sebab keluar", "வெளியேறும் காரணம்", "出场原因"),
    "col.pnl": L("P&L", "Untung/Rugi", "லாபம்/நட்டம்", "盈亏"),
    "col.r_multiple": L("R", "R", "R", "R"),
    "col.note": L("Reason", "Sebab", "காரணம்", "理由"),
    # ------------------------------------------------------------------ price chart
    "chart.source": L("Data source", "Sumber data", "தரவு மூலம்", "数据源"),
    "chart.show_last": L("Show last", "Papar terakhir", "கடைசியாகக் காட்டு", "显示最近"),
    "chart.days": L("{n} days", "{n} hari", "{n} நாட்கள்", "{n} 天"),
    "chart.close": L("Close", "Harga tutup", "முடிவு விலை", "收盘价"),
    "chart.vs": L("price {pct}%", "harga {pct}%", "விலை {pct}%", "价格 {pct}%"),
    "chart.atr_pct": L(
        "{pct}% of price", "{pct}% daripada harga", "விலையின் {pct}%", "占价格 {pct}%"
    ),
    "chart.volume": L("Volume", "Volum", "அளவு", "成交量"),
    "chart.caption": L(
        "Source: {src} · last bar {date}",
        "Sumber: {src} · bar terakhir {date}",
        "மூலம்: {src} · கடைசி பார் {date}",
        "数据源：{src} · 最新K线 {date}",
    ),
    "chart.to_sizer": L(
        "🧮 Use this price and ATR in Position Sizer",
        "🧮 Guna harga dan ATR ini dalam Kalkulator Saiz Posisi",
        "🧮 இந்த விலையையும் ATR-ஐயும் நிலை அளவு கணிப்பானில் பயன்படுத்தவும்",
        "🧮 将此价格和 ATR 用于仓位计算器",
    ),
    # ------------------------------------------------------------------ position sizer
    "sizer.caption": L(
        "Uses skills/position-sizer — the same calculation as the Claude skill.",
        "Menggunakan skills/position-sizer — pengiraan yang sama seperti skill Claude.",
        "skills/position-sizer ஐப் பயன்படுத்துகிறது — Claude திறனின் அதே கணக்கீடு.",
        "调用 skills/position-sizer——与 Claude 技能相同的计算。",
    ),
    "sizer.prefilled": L(
        "Prefilled from Price Chart: {sym} entry {entry}, ATR {atr}",
        "Diisi dari Carta Harga: {sym} masuk {entry}, ATR {atr}",
        "விலை விளக்கப்படத்திலிருந்து நிரப்பப்பட்டது: {sym} நுழைவு {entry}, ATR {atr}",
        "已从价格图表预填：{sym} 入场 {entry}，ATR {atr}",
    ),
    "sizer.method": L("Method", "Kaedah", "முறை", "方法"),
    "sizer.m_stop": L(
        "Stop-loss (fixed %)", "Henti rugi (% tetap)", "நிறுத்த இழப்பு (நிலையான %)", "止损（固定比例）"
    ),
    "sizer.m_atr": L("ATR-based", "Berasaskan ATR", "ATR அடிப்படை", "基于 ATR"),
    "sizer.m_kelly": L("Kelly criterion", "Kriteria Kelly", "Kelly அளவுகோல்", "凯利公式"),
    "sizer.account": L("Account size ($)", "Saiz akaun ($)", "கணக்கு அளவு ($)", "账户规模 ($)"),
    "sizer.entry": L("Entry price", "Harga masuk", "நுழைவு விலை", "入场价"),
    "sizer.stop": L("Stop price", "Harga henti rugi", "நிறுத்த விலை", "止损价"),
    "sizer.risk_pct": L(
        "Risk per trade (%)", "Risiko setiap dagangan (%)", "ஒரு வர்த்தக இடர் (%)", "单笔风险 (%)"
    ),
    "sizer.atr_mult": L("ATR multiplier", "Pengganda ATR", "ATR பெருக்கி", "ATR 倍数"),
    "sizer.win_rate": L("Win rate (0–1)", "Kadar menang (0–1)", "வெற்றி விகிதம் (0–1)", "胜率 (0–1)"),
    "sizer.avg_win": L(
        "Average win (R or $)",
        "Purata menang (R atau $)",
        "சராசரி வெற்றி (R அல்லது $)",
        "平均盈利 (R 或 $)",
    ),
    "sizer.avg_loss": L(
        "Average loss (R or $)",
        "Purata rugi (R atau $)",
        "சராசரி இழப்பு (R அல்லது $)",
        "平均亏损 (R 或 $)",
    ),
    "sizer.kelly_convert": L(
        "Convert to shares (needs entry & stop)",
        "Tukar kepada saham (perlu harga masuk & henti rugi)",
        "பங்குகளாக மாற்றவும் (நுழைவும் நிறுத்தமும் தேவை)",
        "换算为股数（需要入场价和止损价）",
    ),
    "sizer.constraints": L(
        "Portfolio constraints (optional)",
        "Had portfolio (pilihan)",
        "போர்ட்ஃபோலியோ வரம்புகள் (விருப்பம்)",
        "组合约束（可选）",
    ),
    "sizer.max_pos": L(
        "Max position (% of account)",
        "Posisi maks (% akaun)",
        "அதிகபட்ச நிலை (கணக்கின் %)",
        "最大仓位（占账户 %）",
    ),
    "sizer.max_sector": L(
        "Max sector (%)", "Sektor maks (%)", "அதிகபட்சத் துறை (%)", "最大行业占比 (%)"
    ),
    "sizer.sector": L("Sector", "Sektor", "துறை", "行业"),
    "sizer.cur_sector": L(
        "Current sector exposure (%)",
        "Pendedahan sektor semasa (%)",
        "தற்போதைய துறை வெளிப்பாடு (%)",
        "当前行业敞口 (%)",
    ),
    "sizer.fractional": L(
        "Allow fractional shares",
        "Benarkan saham pecahan",
        "பகுதிப் பங்குகளை அனுமதிக்கவும்",
        "允许零碎股",
    ),
    "sizer.calculate": L("Calculate", "Kira", "கணக்கிடு", "计算"),
    "sizer.invalid": L(
        "Invalid input: {err}", "Input tidak sah: {err}", "தவறான உள்ளீடு: {err}", "输入无效：{err}"
    ),
    "sizer.budget": L(
        "Risk budget (half Kelly)",
        "Bajet risiko (separuh Kelly)",
        "இடர் பட்ஜெட் (அரை Kelly)",
        "风险预算（半凯利）",
    ),
    "sizer.pct_acct": L(
        "{pct}% of account", "{pct}% daripada akaun", "கணக்கின் {pct}%", "占账户 {pct}%"
    ),
    "sizer.full_kelly": L("Full Kelly", "Kelly penuh", "முழு Kelly", "全凯利"),
    "sizer.pos_value": L("Position value", "Nilai posisi", "நிலை மதிப்பு", "持仓价值"),
    "sizer.risk_usd": L("Risk ($)", "Risiko ($)", "இடர் ($)", "风险 ($)"),
    "sizer.risk_acct": L(
        "Risk (% of account)", "Risiko (% akaun)", "இடர் (கணக்கின் %)", "风险（占账户 %）"
    ),
    "sizer.stop_used": L(
        "**Stop:** {stop}", "**Henti rugi:** {stop}", "**நிறுத்தம்:** {stop}", "**止损：**{stop}"
    ),
    "sizer.binding": L(
        "Limited by constraint: **{name}**",
        "Dihadkan oleh: **{name}**",
        "வரம்பால் கட்டுப்படுத்தப்பட்டது: **{name}**",
        "受以下约束限制：**{name}**",
    ),
    "sizer.report": L(
        "Full report (English)",
        "Laporan penuh (Bahasa Inggeris)",
        "முழு அறிக்கை (ஆங்கிலம்)",
        "完整报告（英文）",
    ),
    "sizer.download": L(
        "Download report (.md)",
        "Muat turun laporan (.md)",
        "அறிக்கையைப் பதிவிறக்கவும் (.md)",
        "下载报告 (.md)",
    ),
    # ------------------------------------------------------------------ market breadth
    "breadth.caption": L(
        "Runs skills/market-breadth-analyzer on public CSV data — no API key.",
        "Menjalankan skills/market-breadth-analyzer pada data CSV awam — tanpa kunci API.",
        "பொது CSV தரவில் skills/market-breadth-analyzer ஐ இயக்குகிறது — API விசை தேவையில்லை.",
        "基于公开 CSV 数据运行 skills/market-breadth-analyzer——无需 API 密钥。",
    ),
    "breadth.run": L("Run analysis", "Jalankan analisis", "பகுப்பாய்வை இயக்கவும்", "运行分析"),
    "breadth.spinner": L(
        "Fetching breadth data and scoring…",
        "Mengambil data dan mengira skor…",
        "தரவைப் பெற்று மதிப்பிடுகிறது…",
        "正在获取数据并评分……",
    ),
    "breadth.failed": L(
        "Analyzer failed: {err}",
        "Penganalisis gagal: {err}",
        "பகுப்பாய்வி தோல்வியடைந்தது: {err}",
        "分析失败：{err}",
    ),
    "breadth.saved": L(
        "Showing the latest saved report. Click **Run analysis** to refresh.",
        "Memaparkan laporan terakhir yang disimpan. Klik **Jalankan analisis** untuk mengemas kini.",
        "கடைசியாகச் சேமித்த அறிக்கை காட்டப்படுகிறது. புதுப்பிக்க **பகுப்பாய்வை இயக்கவும்** கிளிக் செய்யவும்.",
        "显示最近保存的报告。点击**运行分析**以刷新。",
    ),
    "breadth.none": L(
        "No report yet — click **Run analysis**.",
        "Belum ada laporan — klik **Jalankan analisis**.",
        "இன்னும் அறிக்கை இல்லை — **பகுப்பாய்வை இயக்கவும்** கிளிக் செய்யவும்.",
        "尚无报告——请点击**运行分析**。",
    ),
    "breadth.exposure": L(
        "Equity exposure guidance",
        "Panduan pendedahan ekuiti",
        "பங்கு வெளிப்பாடு வழிகாட்டல்",
        "股票仓位建议",
    ),
    "breadth.strongest": L("Strongest", "Paling kuat", "வலிமையானது", "最强"),
    "breadth.weakest": L("Weakest", "Paling lemah", "பலவீனமானது", "最弱"),
    "breadth.latest": L(
        "Latest data: {date} · generated {gen}",
        "Data terkini: {date} · dijana {gen}",
        "சமீபத்திய தரவு: {date} · உருவாக்கப்பட்டது {gen}",
        "最新数据：{date} · 生成于 {gen}",
    ),
    "breadth.components": L("Components", "Komponen", "கூறுகள்", "分项"),
    "breadth.levels": L(
        "Key levels to watch",
        "Paras penting untuk diperhati",
        "கவனிக்க வேண்டிய முக்கிய நிலைகள்",
        "需关注的关键水平",
    ),
    "breadth.saved_to": L(
        "Reports saved to {path}. Signal text comes from the skill in English.",
        "Laporan disimpan di {path}. Teks isyarat datang daripada skill dalam Bahasa Inggeris.",
        "அறிக்கைகள் {path} இல் சேமிக்கப்பட்டன. சமிக்ஞை உரை திறனிலிருந்து ஆங்கிலத்தில் வருகிறது.",
        "报告保存在 {path}。信号文字由技能以英文生成。",
    ),
    # ------------------------------------------------------------------ catalog
    "catalog.search": L("Search", "Cari", "தேடல்", "搜索"),
    "catalog.placeholder": L(
        "e.g. dividend, breakout, earnings",
        "cth. dividend, breakout, earnings",
        "எ.கா. dividend, breakout, earnings",
        "例如 dividend、breakout、earnings",
    ),
    "catalog.category": L("Category", "Kategori", "வகை", "类别"),
    "catalog.api": L("API requirement", "Keperluan API", "API தேவை", "API 需求"),
    "catalog.count": L(
        "{n} of {total} skills · descriptions are in English",
        "{n} daripada {total} skill · penerangan dalam Bahasa Inggeris",
        "{total} இல் {n} திறன்கள் · விளக்கங்கள் ஆங்கிலத்தில்",
        "{total} 个技能中的 {n} 个 · 描述为英文",
    ),
    "catalog.meta": L(
        "Status: {status} · Timeframe: {tf} · Difficulty: {diff} · {api}",
        "Status: {status} · Jangka masa: {tf} · Kesukaran: {diff} · {api}",
        "நிலை: {status} · காலவரம்பு: {tf} · சிரமம்: {diff} · {api}",
        "状态：{status} · 周期：{tf} · 难度：{diff} · {api}",
    ),
    "catalog.integrations": L("Integrations", "Integrasi", "ஒருங்கிணைப்புகள்", "集成"),
    "api.none": L("No paid API", "Tiada API berbayar", "கட்டண API இல்லை", "无需付费 API"),
    "api.optional": L(
        "Paid API optional", "API berbayar pilihan", "கட்டண API விருப்பம்", "付费 API 可选"
    ),
    "api.required": L(
        "Paid API required", "API berbayar diperlukan", "கட்டண API தேவை", "需要付费 API"
    ),
    "cat.market-regime": L("Market Regime", "Rejim Pasaran", "சந்தை நிலை", "市场状态"),
    "cat.core-portfolio": L("Core Portfolio", "Portfolio Teras", "முக்கிய போர்ட்ஃபோலியோ", "核心组合"),
    "cat.dividend-income": L(
        "Dividend Income", "Pendapatan Dividen", "ஈவுத்தொகை வருமானம்", "股息收入"
    ),
    "cat.swing-opportunity": L("Swing Opportunity", "Peluang Swing", "ஸ்விங் வாய்ப்பு", "波段机会"),
    "cat.trade-planning": L(
        "Trade Planning", "Perancangan Dagangan", "வர்த்தகத் திட்டமிடல்", "交易计划"
    ),
    "cat.trade-memory": L("Trade Memory", "Memori Dagangan", "வர்த்தக நினைவகம்", "交易记录"),
    "cat.strategy-research": L(
        "Strategy Research", "Penyelidikan Strategi", "உத்தி ஆராய்ச்சி", "策略研究"
    ),
    "cat.advanced-satellite": L(
        "Advanced Satellite", "Satelit Lanjutan", "மேம்பட்ட துணை", "进阶卫星策略"
    ),
    "cat.meta": L("Meta", "Meta", "மெட்டா", "元技能"),
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs):
    """Translate `key` into `lang` (falls back to English, then to the key itself)."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    value = entry.get(lang) or entry[DEFAULT_LANG]
    if kwargs and isinstance(value, str):
        return value.format(**kwargs)
    return value
