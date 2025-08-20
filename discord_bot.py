import discord
import asyncio
import logging

class DiscordJobBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = int(channel_id)
        self.client = discord.Client(intents=discord.Intents.default())
        self.loop = asyncio.get_event_loop()
        self.last_error = None

    async def post_jobs(self, jobs):
        try:
            await self.client.login(self.token)
            channel = await self.client.fetch_channel(self.channel_id)
            for job in jobs:
                msg = self.format_job(job)
                await channel.send(msg)
            await self.client.close()
        except Exception as e:
            self.last_error = str(e)
            logging.error(f"Discord bot error: {e}")
            await self.client.close()
            raise

    def format_job(self, job):
        skills = ', '.join(job.get('skills', []))
        payment = job.get('payment')
        if isinstance(payment, dict):
            if 'min_hourly_wage' in payment:
                payment_str = f"{payment['min_hourly_wage']}円〜{payment.get('max_hourly_wage','?')}円/時"
            elif 'min_budget' in payment:
                payment_str = f"{payment['min_budget']}円〜{payment.get('max_budget','?')}円"
            else:
                payment_str = str(payment)
        else:
            payment_str = str(payment)
        return (f"Job ID: {job.get('id')}\n"
                f"Title: {job.get('title')}\n"
                f"Skills: {skills}\n"
                f"Status: {job.get('status')}\n"
                f"Payment: {payment_str}\n"
                f"Added: {job.get('last_released_at')}\n"
                f"Link: {job.get('link')}")

    def run(self, jobs):
        self.loop.run_until_complete(self.post_jobs(jobs))

if __name__ == '__main__':
    import sys, json
    if len(sys.argv) < 4:
        print('Usage: python discord_bot.py jobs.json token channel_id')
        exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        jobs = json.load(f)
    token = sys.argv[2]
    channel_id = sys.argv[3]
    bot = DiscordJobBot(token, channel_id)
    bot.run(jobs) 