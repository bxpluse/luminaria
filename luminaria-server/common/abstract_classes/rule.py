class Rule:

    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.description = ''
        self.rule_names = []
        self.is_running = False
        self.scheduler = None
        self.app_id = None

    def create_subrule(self, name, func, triggers, args=None):
        self.scheduler.create_job(name=name,
                                  app_id=self.app_id,
                                  func=func,
                                  args=args,
                                  triggers=triggers
                                  )
