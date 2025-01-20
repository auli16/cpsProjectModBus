import pytep.siminterface as siminterface

# Configurazione dell'interfaccia della simulazione
si = siminterface.SimInterface().setup()

# Parametri dell'attacco surge
τ = 10  # Soglia
bi = 2  # Parametro bi (ipotetico)
y_i_hat = 7  # Valore stimato y_i(k)
y_min = 3  # Minimo per y_i
y_max = 15  # Massimo per y_i

# Funzione che simula l'attacco surge
def surge_attack(Si_k, τ, bi, y_i_hat, y_min, y_max):
    # Caso in cui Si(k + 1) <= τ
    if Si_k <= τ:
        y_i_tilde = y_min  # La variabile si stabilizza al valore minimo
    else:
        # Caso in cui Si(k + 1) > τ
        y_i_tilde = y_i_hat - abs(τ + bi - Si_k)
    
    # Verifica per y7
    y7_tilde = y_max if Si_k <= τ else y_i_hat + abs(τ + bi - Si_k)
    
    return y_i_tilde, y7_tilde

# Impostiamo i valori iniziali
Si_k = 5  # Valore iniziale di Si(k)

# Avvia la simulazione (ad esempio, per 5 passi)
for step in range(5):
    # Ottieni il valore attuale di Si(k) dalla simulazione
    Si_k = si.get_idv(1)
    
    # Esegui l'attacco surge in base al valore corrente di Si(k)
    y_i_tilde, y7_tilde = surge_attack(Si_k, τ, bi, y_i_hat, y_min, y_max)
    
    # Imposta i nuovi valori per IDV1 e IDV7
    si.set_idv(1, y_i_tilde)
    si.set_idv(7, y7_tilde)

    # Simula l'evoluzione del sistema per un passo
    si.simulate(1)

    # Stampa i risultati del passo
    print(f"Passo {step + 1}:")
    print("y_i_tilde:", y_i_tilde)
    print("y7_tilde:", y7_tilde)
    print("Risultato di Si(k+1):", si.get_idv(1))
    print("Risultato di Si(k+1) per y7:", si.get_idv(7))
