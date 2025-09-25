import discord
import asyncio
import re
from datetime import datetime

active_timer = None
timer_message = None

def create_progress_bar(current, total, length=10):
    """Crée une barre de progression visuelle"""
    if total == 0:
        return "█" * length + " 100%"
    
    filled = int((current / total) * length)
    bar = "█" * filled + "░" * (length - filled)
    percentage = int((current / total) * 100)
    return f"{bar} {percentage}%"

def format_time(seconds):
    """Formate le temps en minutes et secondes"""
    if seconds <= 0:
        return "0m 0s"
    
    minutes = seconds // 60
    secs = seconds % 60
    
    if minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

async def clear_channel_messages(channel):
    """Supprime tous les messages du channel"""
    try:
        messages = []
        async for message in channel.history(limit=None):
            messages.append(message)
        
        for i in range(0, len(messages), 100):
            batch = messages[i:i+100]
            await channel.delete_messages(batch)
            
    except discord.Forbidden:
        print("Erreur : Pas les permissions pour supprimer les messages")
    except Exception as e:
        print(f"Erreur lors du nettoyage du channel : {e}")

async def update_timer_display(channel, user, total_seconds):
    """Met à jour l'affichage du minuteur"""
    global timer_message, active_timer
    
    # Embed initial
    embed = discord.Embed(
        title="Minuteur en cours",
        description=f"Lancé par {user.mention}",
        color=0x00ff00
    )
    embed.add_field(
        name="Temps restant", 
        value=format_time(total_seconds), 
        inline=True
    )
    embed.add_field(
        name="Temps total", 
        value=format_time(total_seconds), 
        inline=True
    )
    embed.add_field(
        name="Progression", 
        value=create_progress_bar(0, total_seconds), 
        inline=False
    )
    embed.timestamp = datetime.now()
    
    timer_message = await channel.send(embed=embed)
    
    for remaining in range(total_seconds, 0, -30):  # Mise à jour toutes les 30 secondes pour éviter le risque de ban
        if active_timer and active_timer.cancelled():
            return
            
        elapsed = total_seconds - remaining
        progress_bar = create_progress_bar(elapsed, total_seconds)
        
        # Modifie la couleur selon le temps restant
        if remaining <= 60:
            color = 0xff0000
        elif remaining <= 300:
            color = 0xff8800
        else:
            color = 0x00ff00
        
        # Mise à jour de l'embed
        embed = discord.Embed(
            title="Minuteur en cours",
            description=f"Lancé par {user.mention}",
            color=color
        )
        embed.add_field(
            name="Temps restant", 
            value=format_time(remaining), 
            inline=True
        )
        embed.add_field(
            name="Temps total", 
            value=format_time(total_seconds), 
            inline=True
        )
        embed.add_field(
            name="Progression", 
            value=progress_bar, 
            inline=False
        )
        embed.timestamp = datetime.now()
        
        try:
            await timer_message.edit(embed=embed)
        except discord.NotFound:
            return
        
        await asyncio.sleep(30)
    
    final_embed = discord.Embed(
        title="Minuteur terminé !",
        description=f"{user.mention} Ton minuteur est terminé !",
        color=0xff0000
    )
    final_embed.add_field(
        name="Durée totale", 
        value=format_time(total_seconds), 
        inline=False
    )
    final_embed.add_field(
        name="Progression", 
        value=create_progress_bar(total_seconds, total_seconds), 
        inline=False
    )
    final_embed.timestamp = datetime.now()
    
    try:
        await timer_message.edit(embed=final_embed)
        await channel.send(f"{user.mention} Minuteur terminé !")
    except discord.NotFound:
        await channel.send(embed=final_embed)
        await channel.send(f"{user.mention} Minuteur terminé !")

async def handle_timer_command(message, bot):
    """Gère les commandes de minuteur"""
    global active_timer, timer_message
    
    # Ignorer les messages du bot pour éviter les boucles infinies
    if message.author == bot.user:
        return
    
    if message.content.lower().strip() == "stop":
        if active_timer and not active_timer.done():
            active_timer.cancel()
            print(f"Minuteur arrêté par {message.author}")
            
            if timer_message:
                embed = discord.Embed(
                    title="Minuteur arrêté",
                    description=f"Arrêté par {message.author.mention}",
                    color=0xff0000
                )
                embed.timestamp = datetime.now()
                
                try:
                    await timer_message.edit(embed=embed)
                except:
                    await message.channel.send(embed=embed)
            
            await message.channel.send(f"Minuteur arrêté par {message.author.mention}")
        else:
            await message.reply("Aucun minuteur en cours !")
        
        try:
            await message.delete()
        except:
            pass
        return True
    
    pattern = r"^\s*(\d+)\s*$"
    match = re.search(pattern, message.content.strip())
    
    if match:
        minutes = int(match.group(1))
        
        if minutes > 120:  # Max 2 heures
            await message.reply("Maximum 120 minutes autorisé !")
            return True
        
        if minutes == 0:
            await message.reply("Minimum 1 minute !")
            return True
        
        if active_timer and not active_timer.done():
            await message.reply("Un minuteur est déjà en cours !")
            return True
        
        try:
            await message.delete()
        except:
            pass
        
        # Nettoyer le channel avant de lancer le minuteur
        await clear_channel_messages(message.channel)
        
        # Lancer le minuteur
        total_seconds = minutes * 60
        active_timer = asyncio.create_task(
            update_timer_display(message.channel, message.author, total_seconds)
        )
        
        print(f"Minuteur de {minutes} minutes lancé par {message.author}")
        return True
    return False
