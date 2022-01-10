#imports
import disnake
from disnake.ext import commands
import random
from db import users, conn
from dotenv import load_dotenv

load_dotenv()
intents=disnake.Intents.all()
bot=commands.Bot(command_prefix="!", intents=intents)

token=os.getenv('token')
welcome_channel=718327643816198168
reaction_channel=718327643816198168
reaction_message=929710124526862397


@bot.event
async def on_ready():
    print(f"Connected to {bot.user}")
    
#Welcoming User
@bot.event
async def on_member_join(member):
	welcome_msg=[f"Welcome {member.mention}", f"{member.name} just joined!", f"Hello {member.name}"]
	channel=bot.get_channel(welcome_channel)
	await channel.send(random.choice(welcome_msg))
	
#Reaction
@bot.event
async def on_raw_reaction_add(payload):
	channel=bot.get_channel(reaction_channel)
	message=await channel.fetch_message(payload.message_id)
	if payload.emoji.id==None:
	   emoji=payload.emoji.name
	else:
	   emoji=f"<:{payload.emoji.name}:{payload.emoji.id}>"
	embed=disnake.Embed(title=f"{emoji}",description=f"{payload.member.name} reacted to {message.author.name}",color=0x66ffcc)
	embed.set_footer(text=channel.name)
	await channel.send(embed=embed)
	
#Create "name" role/empty role
@bot.command()
async def parameter(ctx,name=None):
		    if name==None:
		    	name="new_role"
		    role=disnake.utils.get(ctx.guild.roles, name=name)
		    if role == None:
		    	role=await ctx.guild.create_role(name=name)
		    await ctx.author.add_roles(role)
		    await ctx.send("{role.name} given.")
		    
#Register member/user
@bot.command()
async def register(ctx,member:disnake.Member=None):
		    	if member==None:
		    		member=ctx.author
		    	get=users.select().filter_by(name=member)
		    	data=conn.execute(get).fetchall()
		    	if len(data)==0:
		    		new=users.insert().values(name=name)
		    		conn.execute(new)
		    		await ctx.send(f"{member.name} succesfully registered.")
		    	else:
		    	 	await ctx.send("User already registered.")

#List of registered
@bot.command()
@bot.has_permissions(manage_guild=True)
async def name(ctx):
			embed=disnake.Embed(title="Registered", description="",color=0x66ffcc)
			get=users.select()
			data=conn.execute(get).fetchall()
			for i in range(len(data)):
				embed.add_field(name=i+1,  value=data[i][1])
			await ctx.send(embed=embed)
			
@name.error
async def name_error(ctx,error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("Missing perms")
bot.run(token)