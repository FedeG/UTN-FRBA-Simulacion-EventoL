# UTN FRBA Simulación TP6 EventoL

## Resumen:

Trabajo practivo número 6 de simulación

## Get Started: 🚀

### Instalar entorno virtual

```bash
poetry install
```

### Activar entorno virtual

```bash
poetry shell
```

## Resultados

### run_n_times(1, 0, 100000, 25)

```c
La variable de control es: 1

Porcentaje de tiempo ocioso por puesto
Puesto 0: 1.289706989312532%

Porcentaje de arrepentimiento es de 41.839240877504295%

Promedio de espera en cola: 33.97817562344694 segundos
```

### run_n_times(1, 1, 100000, 25)

```c

La variable de control es: 1
Porcentaje de tiempo ocioso por puesto
Puesto 0: 7.717401601524095%

Porcentaje de arrepentimiento es de 0.9792193139343546%

Promedio de espera en cola: 8.23022214891753 segundos

Tiempos y % de atención en intermitentes
Puesto 0: 30258.293444098068 segundos 21.843822669336056%
```

### run_n_times(2, 0, 100000, 25)

```c
La variable de control es: 2

Porcentaje de tiempo ocioso por puesto
Puesto 0: 30.382693368397295%
Puesto 1: 30.404864014135246%

Porcentaje de arrepentimiento es de 0.4261141702243832%

Promedio de espera en cola: 3.0260856393493496 segundos
```

### run_n_times(2, 1, 100000, 25)

```c
La variable de control es: 2

Porcentaje de tiempo ocioso por puesto
Puesto 0: 34.06836558479106%
Puesto 1: 33.99374945857062%

Porcentaje de arrepentimiento es de 0.004065085928975804%

Promedio de espera en cola: 1.4658082038484554 segundos

Tiempos y % de atención en intermitentes
Puesto 0: 7203.052914522423 segundos 5.170197100222712%
```

### run_n_times(2, 2, 100000, 25)

```c
La variable de control es: 2

Porcentaje de tiempo ocioso por puesto
Puesto 0: 34.27510330594409%
Puesto 1: 34.21589410722592%

Porcentaje de arrepentimiento es de 0.0%

Promedio de espera en cola: 1.3752514142680679 segundos

Tiempos y % de atención en intermitentes
Puesto 0: 4163.812146461198 segundos 2.9834179572407002%
Puesto 1: 4115.739824746659 segundos 2.9489736012504095%
```

### run_n_times(3, 0, 100000, 25)

```c
La variable de control es: 3

Porcentaje de tiempo ocioso por puesto
Puesto 0: 53.25235321160647%
Puesto 1: 53.2895009646774%
Puesto 2: 53.29577239465436%

Porcentaje de arrepentimiento es de 0.0008972658863819711%

Promedio de espera en cola: 0.20234493943797002 segundos
```
