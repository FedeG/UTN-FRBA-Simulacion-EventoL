import random

from scipy.stats import lognorm


HV = float('inf')

def get_IA():
    r = random.uniform(0, 0.9999999)
    mu = 9.32  # Media
    sigma = 0.60776  # Desviación estándar
    inverse_value = lognorm.ppf(r, s=sigma, scale=mu)

    return inverse_value


def get_primera_llegada():
    return get_IA()


def get_TA_con_qr_autogestionada():
    return random.uniform(2, 3)


def get_TA_con_qr_mesa_de_entrada():
    return random.uniform(4, 5)


def get_TA_con_registro_previo():
    return random.uniform(8, 12)


def get_TA_sin_registro_previo():
    return random.uniform(15, 25)


def va_a_instalar():
    r = random.uniform(0, 1)
    return r <= 0.1822279459


def get_TA_extra_por_instalar():
    return random.uniform(5, 10)


def get_proxima_salida(tps):
    return tps.index(min(tps))


def get_puesto_ocioso_hace_mas_tiempo(tps, ito):
    libres = [index for index, time in enumerate(tps) if time == HV]

    if len(libres) == 1:
        return libres[0]

    itos_index = [(ito[index], index) for index in libres]
    itos_index_sorted = sorted(itos_index, key=lambda x: x[0])
    return itos_index_sorted[0][1]


def get_TA():
    qr_autogestionado = 0.0012878300
    qr_mesa_entrada = 0.1294269156
    registro_previo = 0.3657437218
    sin_registro_previo = 0.5035415325
    r = random.uniform(0, 1)

    if 0 <= r <= qr_autogestionado:
        aux = get_TA_con_qr_autogestionada()
    elif r <= qr_autogestionado + qr_mesa_entrada:
        aux = get_TA_con_qr_mesa_de_entrada()
    elif r <= qr_autogestionado + qr_mesa_entrada + registro_previo:
        aux = get_TA_con_registro_previo()
    elif r <= 1:
        # <= qr_autogestionado + qr_mesa_entrada + registro_previo + sin_registro_previo
        aux = get_TA_sin_registro_previo()

    if va_a_instalar():
        aux += get_TA_extra_por_instalar()

    return aux


def get_arrepentimiento(NS, N):
    return NS - N >= 3


def usa_intermitente(NS, N):
    return NS - N >= 2


def run(N, M, TF, log=True):
    TPLL = get_primera_llegada()
    TPS = [HV] * N
    TPSI = [HV] * M
    CPO = 0
    NS = 0
    NT = 0
    AR = 0
    STS = 0
    STLL = 0
    STA = 0
    STAI = [0] * M
    ITO = [0] * N
    ITOI = [0] * M
    STO = [0] * N
    STOI = [0] * M
    PTO = [HV] * N
    T = 0

    while T <= TF or NS > 0:
        if log:
            print(f'T: {T} TF: {TF} NS: {NS} NT: {NT} TPLL: {TPLL} TPS: {TPS}')

        i = get_proxima_salida(TPS)
        j = get_proxima_salida(TPSI) if M > 0 else -1
        if (M > 0 and TPLL <= TPS[i] and TPLL <= TPSI[j]) or (M == 0 and TPLL <= TPS[i]):
            # llegada
            T = TPLL
            IA = get_IA()
            TPLL += IA

            arrepentimiento = get_arrepentimiento(NS, N + CPO)
            if arrepentimiento:
                AR += 1
                continue

            NS += 1
            NT += 1
            STLL += T

            if NS <= N + CPO:
                k = get_puesto_ocioso_hace_mas_tiempo(TPS, ITO)
                TA = get_TA()
                TPS[k] = T + TA+ CPO
                STO[k] = STO[k] + (T - ITO[k])
                STA += TA
            elif M > 0 and usa_intermitente(NS, N + CPO) and NS <= N + M + 2:
                if M - CPO > 0:
                    k = get_puesto_ocioso_hace_mas_tiempo(TPSI, ITOI)
                    TA = get_TA()
                    TPSI[k] = T + TA
                    STOI[k] = STOI[k] + (T - ITOI[k])
                    STA += TA
                    STAI[k] += TA
                    CPO += 1
        else:
            # salida
            if M > 0 and TPSI[j] <= TPS[i]:
                # salida intermitente
                T = TPSI[j]
                STS += T
                NS -= 1
                CPO -= 1

                if usa_intermitente(NS, N + CPO - 1):
                    TA = get_TA()
                    TPSI[j] = T + TA
                    STA += TA
                    CPO += 1
                else:
                    TPSI[j] = HV
                    ITOI[j] = T
            else:
                # salida fijos
                T = TPS[i]
                STS += T
                NS -= 1

                if NS >= N + CPO:
                    TA = get_TA()
                    TPS[i] = T + TA
                    STA += TA
                else:
                    TPS[i] = HV
                    ITO[i] = T
        if T > TF:
            TPLL = HV

    SPS = STS - STLL
    STE = SPS - STA
    for j in range(0, N):
        PTO[j] = STO[j] * 100 / T
    PEC = STE / NT
    PA = AR * 100 / NT

    if log:
        print(f'La variable de control es: {N}')
        print(f'Porcentaje de tiempo ocioso por puesto')
        for l in range(0, N):
            print(f'Puesto {l}: {PTO[l]}%')
        print(f'Porcentaje de arrepentimiento es de {PA}%')
        print(f'Promedio de espera en cola: {PEC} segundos')
        if M > 0:
            print(f'Tiempos de atención en intermitentes: {STAI} segundos')

    return N, TF, PTO, PA, PEC, STAI, STA


def run_n_times(N, M, TF, n):
    # results = [(N, TF, PTO, PA, PEC)]
    results = [run(N, M, TF, log=False) for _ in range(n)]

    print(f'La variable de control es: {N}')
    print(f'Porcentaje de tiempo ocioso por puesto')
    for l in range(0, N):
        PTOS = [result[2][l] for result in results]
        PTO_MEAN = sum(PTOS) / len(PTOS)
        print(f'Puesto {l}: {PTO_MEAN}%')

    PAS = [result[3] for result in results]
    PA_MEAN = sum(PAS) / len(PAS)
    print(f'Porcentaje de arrepentimiento es de {PA_MEAN}%')

    PECS = [result[4] for result in results]
    PEC_MEAN = sum(PECS) / len(PECS)
    print(f'Promedio de espera en cola: {PEC_MEAN} segundos')

    if M > 0:
        print(f'Tiempos y % de atención en intermitentes')
        for l in range(0, M):
            STAIS = [result[5][l] for result in results]
            STAIO_MEAN = sum(STAIS) / len(STAIS)
            STAS = [result[6] for result in results]
            STA_MEAN = sum(STAS) / len(STAS)
            print(f'Puesto {l}: {STAIO_MEAN} segundos {STAIO_MEAN*100/STA_MEAN}%')
