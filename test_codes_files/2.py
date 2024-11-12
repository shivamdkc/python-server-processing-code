from datetime import datetime, timedelta
from typing import List, Dict

class Process:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

class Fabric:
    def __init__(self, name: str, fabric_type: str, processes: List[Process], quantity: int):
        self.name = name
        self.fabric_type = fabric_type
        self.processes = processes
        self.quantity = quantity

class Stage:
    def __init__(self, process: Process, start_date: datetime, end_date: datetime):
        self.process = process
        self.start_date = start_date
        self.end_date = end_date

class Order:
    def __init__(self, order_date: datetime, fabrics: List[Fabric]):
        self.order_date = order_date
        self.fabrics = fabrics

class Scheduler:
    def __init__(self, order: Order):
        self.order = order
        self.schedule = {}

    def calculate_end_date(self, start_date: datetime, duration: int) -> datetime:
        return start_date + timedelta(days=duration)

    def process_fabric(self, fabric: Fabric, start_date: datetime) -> Dict[str, Stage]:
        current_date = start_date
        process_dates = {}

        for process in fabric.processes:
            end_date = self.calculate_end_date(current_date, process.duration)
            process_dates[process.name] = Stage(process, current_date, end_date)
            current_date = end_date

        return process_dates

    def schedule_fabrics(self):
        fabrics = sorted(self.order.fabrics, key=lambda f: f.quantity, reverse=True)
        major_fabric = fabrics[0]
        minor_fabrics = fabrics[1:]

        if major_fabric.fabric_type == "International":
            # Skip all stages for international major fabric
            for fabric in minor_fabrics:
                if fabric.fabric_type == "Indian":
                    minor_process_dates = self.process_fabric(fabric, self.order.order_date)
                    self.schedule[fabric.name] = minor_process_dates
            return

        major_process_dates = self.process_fabric(major_fabric, self.order.order_date)
        self.schedule[major_fabric.name] = major_process_dates

        for fabric in minor_fabrics:
            if fabric.fabric_type == "International":
                # Skip all stages for international minor fabric
                continue
            
            start_date = self.order.order_date
            if "print" in [p.name for p in major_fabric.processes]:
                start_date = major_process_dates["print"].end_date

            if "emb" in [p.name for p in fabric.processes]:
                minor_process_dates = self.process_fabric(fabric, start_date)
            else:
                if "dying" in [p.name for p in fabric.processes]:
                    if "dying" in [p.name for p in major_fabric.processes]:
                        dying_start_date = major_process_dates["dying"].end_date
                        minor_process_dates = self.process_fabric(fabric, dying_start_date)
                    else:
                        minor_process_dates = self.process_fabric(fabric, start_date)
                else:
                    minor_process_dates = self.process_fabric(fabric, start_date)

            self.schedule[fabric.name] = minor_process_dates

    def get_schedule(self):
        return self.schedule

# Sample usage
process_print = Process("print", 5)
process_emb = Process("emb", 3)
process_dying = Process("dying", 7)

fabric1 = Fabric("Fabric A", "Indian", [process_print, process_emb, process_dying], 100)
fabric2 = Fabric("Fabric B", "Indian", [process_emb, process_dying], 50)
fabric3 = Fabric("Fabric C", "International", [], 70)

order_date = datetime(2024, 1, 1)
order = Order(order_date, [fabric1, fabric2, fabric3])

scheduler = Scheduler(order)
scheduler.schedule_fabrics()

schedule = scheduler.get_schedule()
for fabric_name, stages in schedule.items():
    print(f"Schedule for {fabric_name}:")
    for stage_name, stage in stages.items():
        print(f"  {stage_name}: {stage.start_date} to {stage.end_date}")
