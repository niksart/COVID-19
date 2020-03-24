# imposta la regione scelta ed esegui lo script

interested_region = "Veneto"

# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

seaborn.set_style("dark")

# auxiliary functions

def parse_data(s):
    s = s.split(" ")[0]
    mese = s.split("-")[1]
    giorno = s.split("-")[2]
    
    return giorno + "/" + str(int(mese))

# 0: regione_nuovi/tamponi
# 1: provincia totali e logaritmo totali TODO
plot_type = 0

regioni_csv = pd.read_csv("dati-regioni/dpc-covid19-ita-regioni.csv")

if plot_type == 0:
    # --------------- OBTAIN DATA -------------------------------------
    
    regione_csv = regioni_csv[regioni_csv["denominazione_regione"]==interested_region]
    # ottengo gioni
    giorni = list(map(parse_data, regione_csv["data"].values))
    
    # nuovi attualmente positivi all'interno della regione
    nuovi_positivi = regione_csv["nuovi_attualmente_positivi"].values
    
    # ottengo il numero dei nuovi tamponi giornalieri
    numero_tamponi = regione_csv["tamponi"].values
    delta_tamponi = [numero_tamponi[0]]
    for g in range(len(numero_tamponi) - 1):
        delta_tamponi += [numero_tamponi[g+1] - numero_tamponi[g]]
    
    # percentuale nuovi_positivi/nuovi_tamponi
    div = lambda x: x[0]/x[1] if 0<(x[0]/x[1])<1 else None
    perc_nuovi_pos_nuovi_tamp = list(map(div, list(zip(nuovi_positivi, delta_tamponi))))
    
    # --------------- END OBTAIN DATA ---------------------------
    w = 0.3
    fig, ax1 = plt.subplots()
    
    ind = np.arange(len(giorni))
    
    ax1.set_xlabel("Giorni")
    ax1.set_ylabel("Unità")
    bar_pos = ax1.bar(ind+w, nuovi_positivi, color="tab:red", width=w)
    bar_tamp = ax1.bar(ind, delta_tamponi, color="tab:grey", width=w)
    ax1.tick_params(axis='y')
    
    ax1.set_xticks(ind+(w/2))
    ax1.set_xticklabels(giorni)
    ax1.legend( (bar_pos, bar_tamp), ('Nuovi positivi', 'Nuovi tamponi') )
    ax1.set_xticks([])

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue'
    ax2.set_ylabel('Nuovi positivi / nuovi tamponi', color=color)  # we already handled the x-label with ax1
    line_perc = ax2.plot(giorni, perc_nuovi_pos_nuovi_tamp, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(20, 5)
    plt.title(interested_region + ": confronto giornaliero tra nuovi positivi e nuovi tamponi")
    plt.show()
        
