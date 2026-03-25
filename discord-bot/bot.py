import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO', 'ron1120/basic-cloud-deployment')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


DEPLOY_CHANNEL_ID = 1377709832085180428

GITHUB_API_BASE = 'https://api.github.com'


def github_headers():
    headers = {'Accept': 'application/vnd.github+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'
    return headers


@client.event
async def on_ready():
    print(f'{client.user} is online!')
    channel = client.get_channel(DEPLOY_CHANNEL_ID)
    if channel:
        await channel.send('✅ Bot has been deployed and is online!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!hi':
        await message.channel.send(f'Hello, {message.author.name}!')

    if message.content == '!ping':
        await message.channel.send('Pong!')

    if message.content == '!git repo':
        resp = requests.get(f'{GITHUB_API_BASE}/repos/{GITHUB_REPO}', headers=github_headers(), timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            msg = (
                f"**{data['full_name']}**\n"
                f"{data.get('description') or 'No description'}\n"
                f"⭐ Stars: {data['stargazers_count']} | "
                f"🍴 Forks: {data['forks_count']} | "
                f"🐛 Open issues: {data['open_issues_count']}\n"
                f"🔗 {data['html_url']}"
            )
        else:
            error_detail = resp.json().get('message', resp.text)
            msg = f'❌ Could not fetch repo info (HTTP {resp.status_code}): {error_detail}'
        await message.channel.send(msg)

    if message.content == '!git commits':
        resp = requests.get(
            f'{GITHUB_API_BASE}/repos/{GITHUB_REPO}/commits',
            headers=github_headers(),
            params={'per_page': 5},
            timeout=10,
        )
        if resp.status_code == 200:
            commits = resp.json()
            lines = [f"**Recent commits for `{GITHUB_REPO}`:**"]
            for c in commits:
                sha = c['sha'][:7]
                msg_text = c['commit']['message'].splitlines()[0][:72]
                author = c['commit']['author']['name']
                lines.append(f"`{sha}` {msg_text} — *{author}*")
            msg = '\n'.join(lines)
        else:
            error_detail = resp.json().get('message', resp.text)
            msg = f'❌ Could not fetch commits (HTTP {resp.status_code}): {error_detail}'
        await message.channel.send(msg)

    if message.content == '!git latest':
        resp = requests.get(
            f'{GITHUB_API_BASE}/repos/{GITHUB_REPO}/commits',
            headers=github_headers(),
            params={'per_page': 1},
            timeout=10,
        )
        if resp.status_code == 200:
            commits = resp.json()
            if not commits:
                msg = f'No commits found for `{GITHUB_REPO}`.'
            else:
                c = commits[0]
                sha = c['sha'][:7]
                msg_text = c['commit']['message'].splitlines()[0]
                author = c['commit']['author']['name']
                date = c['commit']['author']['date']
                url = c['html_url']
                msg = (
                    f"**Latest commit on `{GITHUB_REPO}`**\n"
                    f"`{sha}` {msg_text}\n"
                    f"👤 {author} | 📅 {date}\n"
                    f"🔗 {url}"
                )
        else:
            error_detail = resp.json().get('message', resp.text)
            msg = f'❌ Could not fetch latest commit (HTTP {resp.status_code}): {error_detail}'
        await message.channel.send(msg)


client.run(TOKEN)
