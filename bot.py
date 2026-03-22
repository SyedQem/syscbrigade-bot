import discord
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_NAME = "Aria"  # Change this to whatever you want to call your bot

# --- Setup Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        f"You are {BOT_NAME}, a helpful and friendly Discord bot. "
        "Keep responses concise and conversational. "
        "You are part of a Discord server and talking to its members."
    )
)

# Stores conversation history per channel (in-memory, resets on restart)
conversation_history = {}

# --- Discord Setup ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Only respond when mentioned or in DMs
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mentioned = client.user in message.mentions

    if not is_dm and not is_mentioned:
        return

    # Clean the message (strip the @mention)
    user_input = message.content.replace(f"<@{client.user.id}>", "").strip()

    if not user_input:
        await message.reply(f"Hey! Mention me with a message and I'll respond. Try: @{BOT_NAME} what can you do?")
        return

    # Get or create conversation history for this channel
    channel_id = message.channel.id
    if channel_id not in conversation_history:
        conversation_history[channel_id] = []

    # Show typing indicator while generating
    async with message.channel.typing():
        try:
            # Build message history for context
            chat = model.start_chat(history=conversation_history[channel_id])
            response = chat.send_message(user_input)
            reply = response.text

            # Save updated history (keep last 10 exchanges to avoid hitting limits)
            conversation_history[channel_id] = chat.history[-20:]

            # Discord has a 2000 char limit — split if needed
            if len(reply) > 1900:
                chunks = [reply[i:i+1900] for i in range(0, len(reply), 1900)]
                for chunk in chunks:
                    await message.reply(chunk)
            else:
                await message.reply(reply)

        except Exception as e:
            print(f"Error: {e}")
            await message.reply("Sorry, I hit an error. Try again in a moment!")


# --- Slash Commands ---
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    try:
        await tree.sync()
        print("✅ Slash commands synced")
    except Exception as e:
        print(f"Could not sync slash commands: {e}")


@tree.command(name="ask", description="Ask the AI a question")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        response = model.generate_content(question)
        await interaction.followup.send(f"**Q: {question}**\n\n{response.text}")
    except Exception as e:
        await interaction.followup.send("Sorry, something went wrong!")


@tree.command(name="clear", description="Clear my conversation memory for this channel")
async def clear(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    if channel_id in conversation_history:
        del conversation_history[channel_id]
    await interaction.response.send_message("🧹 Memory cleared for this channel!")


client.run(DISCORD_TOKEN)
