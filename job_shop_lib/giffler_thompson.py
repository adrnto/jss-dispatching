sclass GifflerThompsonScheduler:
    def __init__(self, instance, machines):
        # Desempaquetar los trabajos de la instancia
        self.jobs = instance.jobs  # Asignar los trabajos de la instancia de JobShop
        self.machines = machines
        self.schedule = []  # Cronograma final que será generado por el algoritmo

    def schedule_operations(self):
        """Aplica el algoritmo Giffler & Thompson para programar las operaciones."""
        while any(job.has_pending_operations() for job in self.jobs):
            feasible_operations = self.find_feasible_operations()
            selected_operation = self.select_operation(feasible_operations)
            self.schedule.append(selected_operation)  # Añadir la operación al cronograma
    def find_feasible_operations(self):
        """Encuentra las operaciones que pueden ser ejecutadas."""
        feasible_operations = []
        for job in self.jobs:
            if job.has_ready_operations():  # Verificar si el trabajo tiene operaciones listas para ejecutarse
                feasible_operations.append(job.get_next_operation())
        return feasible_operations

    def select_operation(self, feasible_operations):
        """
        Selecciona la operación más prometedora basada en la menor fecha de finalización.
        
        :param feasible_operations: Lista de operaciones factibles.
        :return: Operación seleccionada.
        """
        return min(feasible_operations, key=lambda op: op.get_duration())

    def schedule_operations(self):
        """Aplica el algoritmo G&T para programar todas las operaciones."""
        while any(job.has_pending_operations() for job in self.jobs):
            feasible_operations = self.find_feasible_operations()
            selected_operation = self.select_operation(feasible_operations)
            self.assign_operation(selected_operation)
            self.update_schedule(selected_operation)

    def assign_operation(self, operation):
        """
        Asigna la operación a una máquina disponible.
        :param operation: Operación seleccionada.
        """
        machine = operation.get_machine_id()
        start_time = self.get_next_available_time(machine)
        end_time = start_time + operation.get_duration()
        self.schedule.append({
            'job_id': operation.get_job_id(),
            'operation_id': operation.id,
            'machine_id': machine,
            'start_time': start_time,
            'end_time': end_time
        })

    def get_next_available_time(self, machine_id):
        """
        Obtiene el siguiente tiempo disponible para una máquina.
        :param machine_id: ID de la máquina.
        :return: Tiempo disponible.
        """
        machine_operations = [op for op in self.schedule if op['machine_id'] == machine_id]
        if not machine_operations:
            return 0
        return max(op['end_time'] for op in machine_operations)

    def update_schedule(self, operation):
        """Actualiza el cronograma tras asignar una operación."""
        operation.mark_completed()
