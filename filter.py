import json
import os

class JobFilter:
    def __init__(self, lower_price, upper_price, seen_file='seen_jobs.json'):
        self.lower_price = lower_price
        self.upper_price = upper_price
        self.seen_file = seen_file
        self.seen_ids = set()
        self._load_seen()

    def _load_seen(self):
        if os.path.exists(self.seen_file):
            with open(self.seen_file, 'r', encoding='utf-8') as f:
                self.seen_ids = set(json.load(f))

    def _save_seen(self):
        with open(self.seen_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.seen_ids), f)

    def filter_jobs(self, jobs):
        new_jobs = []
        for job in jobs:
            payment = job.get('payment')
            if not payment:
                continue
            # Handle both hourly and fixed price payments
            if isinstance(payment, dict):
                if 'min_hourly_wage' in payment:
                    price = payment.get('min_hourly_wage', 0)
                elif 'min_budget' in payment:
                    price = payment.get('min_budget', 0)
                else:
                    continue
            elif isinstance(payment, (int, float)):
                price = payment
            else:
                continue
            if not (self.lower_price <= price <= self.upper_price):
                continue
            if job['id'] in self.seen_ids:
                continue
            new_jobs.append(job)
            self.seen_ids.add(job['id'])
        self._save_seen()
        return new_jobs

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('Usage: python filter.py jobs.json lower_price upper_price')
        exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    lower = int(sys.argv[2])
    upper = int(sys.argv[3])
    ftr = JobFilter(lower, upper)
    filtered = ftr.filter_jobs(jobs)
    print(json.dumps(filtered, ensure_ascii=False, indent=2)) 