import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# --- Download Data ---
tickers = ['BHARTIARTL.NS', 'MARUTI.NS', 'M&M.NS', 'ASHOKLEY.NS', 'LT.NS','TVSMOTOR.NS','JSWSTEEL.NS','INDIANB.NS','MUTHOOTFIN.NS','EICHERMOT.NS']
start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
raw_data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', progress=False)

# --- GUI Setup ---
root = tk.Tk()
root.title("TRENDTRACKER: Predictive Terminal")
root.geometry("1200x900")

# --- MODERN DARK THEME PALETTE ---
BG_DARK = "#0f111a"      # Very dark background
BG_MID = "#1a1c2c"       # Slightly lighter for frames/containers
BG_INPUT = "#2c3241"     # Distinct dark background for input fields
ACCENT_COLOR = "#00ffcc" # Neon Cyan for highlights (High-Tech Feel)
TEXT_LIGHT = "white"     # White text
TEXT_DARK = "black"      # Black text for contrast on accent color
ERROR_COLOR = "crimson"  # Red for errors/alerts

root.configure(bg=BG_DARK)

# --- Ttk Style Configuration (Styled for modern dark theme) ---
style = ttk.Style()
style.theme_use("clam") 

# General Label Style
style.configure("TLabel", background=BG_DARK, foreground=TEXT_LIGHT, font=("Consolas", 11))

# Frame/Labelframe Style (Containers)
style.configure("TFrame", background=BG_DARK) 
style.configure("Cool.TLabelframe.Label", 
    background=BG_MID, 
    foreground=ACCENT_COLOR, 
    font=("Consolas", 14, "bold"),
    padding=[10, 5, 10, 5] 
)
style.configure("Cool.TLabelframe", 
    background=BG_MID, 
    foreground=ACCENT_COLOR, 
    bordercolor=ACCENT_COLOR,
    relief="solid", 
    borderwidth=1
)
style.map("Cool.TLabelframe", background=[('active', BG_MID)])

# Button Style
style.configure("TButton", background=ACCENT_COLOR, foreground="black", font=("Consolas", 11, "bold"), borderwidth=0, relief="flat")
style.map("TButton", background=[('active', '#00cccc')], foreground=[('active', 'black')])

# --- TCombobox Styling ---
style.configure("TCombobox", 
    fieldbackground=BG_INPUT,           
    background=BG_INPUT, 
    foreground=TEXT_LIGHT,              
    selectbackground=ACCENT_COLOR, 
    selectforeground=TEXT_DARK,         
    font=("Consolas", 11),
    bordercolor=ACCENT_COLOR 
)
style.map("TCombobox", 
    selectbackground=[('readonly', ACCENT_COLOR)],
    fieldbackground=[('readonly', BG_INPUT)],
    background=[('readonly', BG_INPUT)],
    foreground=[('readonly', TEXT_LIGHT)]
)

# Radiobutton Style
style.configure("TRadiobutton", background=BG_MID, foreground=TEXT_LIGHT, font=("Consolas", 11))
style.map("TRadiobutton", indicatorcolor=[('selected', ACCENT_COLOR)], background=[('active', BG_MID), ('!active', BG_MID)])
style.configure("Input.TRadiobutton", background=BG_MID)
style.map("Input.TRadiobutton", background=[('active', BG_MID), ('!active', BG_MID)])


# --- Layout Frames ---
main_frame = tk.Frame(root, bg=BG_DARK)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Input Frame
input_frame = ttk.LabelFrame(main_frame, text="📊 FORECAST PARAMETERS", style="Cool.TLabelframe")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
inner_input_frame = ttk.Frame(input_frame, style="TFrame")
inner_input_frame.pack(padx=5, pady=5, fill='both', expand=True)

# Output Frame
output_frame = ttk.LabelFrame(main_frame, text="📋 ANALYSIS REPORT", style="Cool.TLabelframe")
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

chart_frame = ttk.LabelFrame(main_frame, text="📈 PRICE VISUALIZATION", style="Cool.TLabelframe")
chart_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# --- Live Ticker Strip ---
ticker_strip = tk.Label(root, 
    text="LIVE TERMINAL FEED: TATASTEEL ₹142.50 ▲ (+1.2%) | MARUTI ₹9,850.00 ▼ (-0.5%) | M&M ₹1,720.00 ▲ (+2.1%)",
    font=("Consolas", 10, "bold"), 
    fg=ACCENT_COLOR, 
    bg=BG_MID, 
    pady=5
)
ticker_strip.pack(fill="x", ipady=3)

# --- Input Widgets ---
ticker_var = tk.StringVar(value=tickers[0])
ttk.Label(inner_input_frame, text="STOCK TICKER:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

# FIX: Removed highlightthickness, highlightbackground, and highlightcolor from ttk.Combobox
ticker_menu = ttk.Combobox(inner_input_frame, textvariable=ticker_var, values=tickers, state="readonly", width=25)
ticker_menu.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(inner_input_frame, text="TARGET DATE (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
# Kept highlight settings for the standard tk.Entry (date_entry) as these are valid for tk widgets.
date_entry = tk.Entry(inner_input_frame, width=28, bg=BG_INPUT, fg=TEXT_LIGHT, insertbackground=ACCENT_COLOR, 
                      font=("Consolas", 11), relief="solid", bd=1, highlightthickness=2, 
                      highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_COLOR, borderwidth=1)
date_entry.grid(row=1, column=1, padx=10, pady=5)
default_date = (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d')
date_entry.insert(0, default_date) 

export_var = tk.StringVar(value="4")
ttk.Label(inner_input_frame, text="EXPORT REPORT:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
export_options = ["Excel (.xlsx)", "CSV (.csv)", "Both", "No export"]
for i, text in enumerate(export_options, start=1):
    ttk.Radiobutton(inner_input_frame, text=text, variable=export_var, value=str(i), style="Input.TRadiobutton").grid(row=2+i, column=0, columnspan=2, sticky="w", padx=20)

forecast_btn = ttk.Button(inner_input_frame, text=">> EXECUTE FORECAST <<", command=lambda: forecast())
forecast_btn.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew", padx=10)


# --- Output Text ---
output_text = tk.Text(output_frame, height=15, width=60, bg=BG_DARK, fg=TEXT_LIGHT, font=("Consolas", 10), bd=0, padx=10, pady=10, relief="flat")
output_text.pack(padx=10, pady=10, fill="both", expand=True)

# Tags for coloring output text
output_text.tag_config('success', foreground='lime')
output_text.tag_config('warning', foreground='yellow')
output_text.tag_config('error', foreground=ERROR_COLOR)
output_text.tag_config('header', foreground=ACCENT_COLOR, font=("Consolas", 11, "bold"))
output_text.insert(tk.END, "STATUS: Ready to receive inputs.\n", 'success')

canvas_widget = None

# --- Forecast Function ---
def forecast():
    global canvas_widget

    target_ticker = ticker_var.get()
    target_date_str = date_entry.get()

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"STATUS: Analyzing {target_ticker}...\n", 'warning')

    if not target_ticker:
        messagebox.showerror("Error", "Please select a stock ticker.")
        output_text.insert(tk.END, "ERROR: Ticker not selected.\n", 'error')
        return

    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
        if target_date <= datetime.today():
             raise ValueError("Target date must be in the future.")
    except ValueError as e:
        messagebox.showerror("Invalid Date", f"Error: {str(e)}\nFormat must be YYYY-MM-DD.")
        output_text.insert(tk.END, f"ERROR: Invalid date input: {e}\n", 'error')
        return

    # --- Data Retrieval & Model ---
    try:
        if len(tickers) > 1 and isinstance(raw_data.columns, pd.MultiIndex):
            df = raw_data[target_ticker]
        else:
            df = raw_data
        
        df = df[['Close', 'Volume']].dropna()
        if df.empty or len(df) < 2:
            raise ValueError("Insufficient historical data for modeling.")

        df['Days'] = (df.index - df.index[0]).days
        X = df['Days'].values.reshape(-1, 1)
        y = df['Close'].values
        model = LinearRegression().fit(X, y) #BACCHA CALL KARU

        target_num = (target_date - df.index[0]).days
        base_prediction = float(model.predict([[target_num]])[0])

        initial_price = df['Close'].iloc[0]
        final_price = df['Close'].iloc[-1]
        years = (df.index[-1] - df.index[0]).days / 365.25
        cagr = (final_price / initial_price) ** (1 / years) - 1 if initial_price > 0 and years > 0 else 0.0

        years_ahead = (target_date - datetime.today()).days / 365.25
        predicted_price = base_prediction * ((1 + cagr) ** years_ahead)

        current_price = float(df['Close'].iloc[-1])
        stop_loss = round(current_price * 0.97, 2)

        # --- Recommendation Logic ---
        if predicted_price > current_price * 1.05:
            recommendation, rec_tag = "STRONG BUY", 'success'
        elif predicted_price > current_price * 1.01:
            recommendation, rec_tag = "BUY", 'success'
        elif predicted_price < current_price * 0.98:
            recommendation, rec_tag = "SELL", 'error'
        else:
            recommendation, rec_tag = "HOLD", 'warning'
            
    except Exception as e:
        messagebox.showerror("Processing Error", f"Failed to process data: {e}")
        output_text.insert(tk.END, f"ERROR: Processing failed: {e}\n", 'error')
        return

    # --- Output Display ---
    output_text.insert(tk.END, f"\n--- {target_ticker} FORECAST REPORT ---\n", 'header')
    output_text.insert(tk.END, f"Current Price.......: ₹{current_price:.4f}\n")
    output_text.insert(tk.END, f"Target Date.........: {target_date.date()}\n")
    output_text.insert(tk.END, f"Predicted Price.....: ₹{predicted_price:.4f}\n", 'warning')
    output_text.insert(tk.END, f"5-Year CAGR Used....: {cagr*100:.2f}%\n")
    output_text.insert(tk.END, f"STOP LOSS LEVEL.....: ₹{stop_loss:.2f}\n\n", 'error')
    output_text.insert(tk.END, f"ACTION RECOMMENDATION: {recommendation}\n", rec_tag)
    output_text.insert(tk.END, f"\nSTATUS: Analysis complete. Report generated.\n", 'success')

    # --- Export Data ---
    export_data = [{'Ticker': target_ticker, 'Date': target_date.date(), 'Predicted Price': round(predicted_price, 4), 'Current Price': round(current_price, 4), 'Stop Loss': stop_loss, 'Recommendation': recommendation}]
    export_df = pd.DataFrame(export_data)
    
    choice = int(export_var.get())
    filename_base = f"{target_ticker}_prediction_{target_date.date()}"
    if choice == 1: export_df.to_excel(f"{filename_base}.xlsx", index=False)
    elif choice == 2: export_df.to_csv(f"{filename_base}.csv", index=False)
    elif choice == 3:
        export_df.to_csv(f"{filename_base}.csv", index=False)
        export_df.to_excel(f"{filename_base}.xlsx", index=False)


    # --- Chart Plotting (Reverted to Preferred Style) ---
    if canvas_widget is not None:
        canvas_widget.get_tk_widget().destroy()
        canvas_widget = None

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))

    # Background and Spine colors
    fig.patch.set_facecolor(BG_MID)
    ax.set_facecolor(BG_MID)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    # Plot data - LIME and GREEN (Preferred Style)
    ax.plot(df.index, df['Close'], color='lime', linewidth=2, label='Daily Close')
    ax.fill_between(df.index, df['Close'], color='green', alpha=0.2)
    
    # Plot Prediction Line/Point - CRIMSON (Preferred Style)
    ax.axvline(target_date, color='crimson', linestyle='--', linewidth=1.5, label='Target Date')
    ax.scatter(target_date, predicted_price, color='crimson', s=60, zorder=5, label='Predicted Price')
    ax.text(target_date, predicted_price, f" ₹{predicted_price:.2f}", fontsize=10, color='crimson', va='bottom', ha='left')
    
    # Plot Trend Line (Gold)
    ax.plot(df.index, model.predict(X), color='gold', linestyle='-', linewidth=1, label='Linear Trend')
    
    ax.set_title(f"Daily Closing Price for {target_ticker}", fontsize=14, fontweight='bold')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (₹)")
    ax.legend(loc='upper left', frameon=False, fontsize=9)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 

    # --- Embed Plot ---
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget = canvas
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# --- Start GUI ---
if __name__ == '__main__':
    root.mainloop()
