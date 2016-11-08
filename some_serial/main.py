import asyncio

import click
import trafaret as t

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from yaml import load


from .bot import init as bot_init
from .connection import create_serial_connection, Output

dev = '/dev/cu.BT_1-DevB'
baudrate = 38400
BOT_TOKEN = "190670250:AAEusYil3XQQ6S0w0XDTseKDGOSAfIgAi_k"
q = asyncio.Queue()


configuration = t.Dict({
    'telegram': t.Dict({
        'token': t.String,
    }),
    'device': t.Dict({
        'dev': t.String,
        'baudrate': t.Int,
    })
})


async def main(loop, config):
    bot_token = config['telegram']['token']
    device = config['device']['dev']
    baudrate = config['device']['baudrate']

    telegram_bot = bot_init(loop, bot_token)

    await create_serial_connection(loop, q, Output, device, baudrate=baudrate)

    while True:
        try:
            message = q.get_nowait()
            print(message)
        except asyncio.QueueEmpty:
            pass

        loop.create_task(telegram_bot.get_updates())
        await asyncio.sleep(3)


@click.command()
@click.option('--config', '-c', default='config.yaml', type=click.Path(exists=True, readable=True),
              help="Configuration path")
def run(config):
    with open(config, 'rb') as fp:
        conf_data = load(fp.read(), Loader=Loader)
    conf_data = configuration.check(conf_data)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, conf_data))
    loop.run_forever()
    loop.close()
