# Agenda Presidencial 🇵🇪 Scrapper
Scrapper para obtener las actividades que se muestran en la agenda presidencial de Perú.

## Permite:
### Obtener las actividades de la semana actual
```python
from classes.scrapper import Scrapper
scrapper = Scrapper()
scrapper.get_current_activities()
```

### Obtener las actividades hasta un periodo 
```python
from classes.scrapper import Scrapper
scrapper = Scrapper()
scrapper.get_history_data(last_day=1, last_month=4, last_year=2024)
```

## Pendiente:
- Exportar información en CSV