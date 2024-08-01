import discord
from discord.ext import commands
from bot.database.database_functions import create_role, assign_role, remove_role, get_role_by_name, get_role_permissions, update_role_permissions
from bot.utils.role_utils import validate_role_name

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="createrole", help="Create a new role with specified properties.")
    @commands.has_permissions(manage_roles=True)
    async def create_role_command(self, ctx, role_name: str, color: discord.Color = None, permissions: str = None):
        """
        Handles the !createrole command, creating a new role with specified properties.

        Args:
            ctx (commands.Context): The context of the command invocation.
            role_name (str): The name of the new role.
            color (discord.Color, optional): The color of the new role. Defaults to None.
            permissions (str, optional): A string representing the permissions of the new role. Defaults to None.

        Returns:
            None
        """
        try:
            if not validate_role_name(role_name):
                await ctx.send(f"Invalid role name. Role names must be alphanumeric and cannot contain spaces.")
                return

            if permissions:
                try:
                    permissions = permissions.split(",")
                    permission_dict = {}
                    for permission in permissions:
                        permission = permission.strip().lower()
                        if hasattr(discord.Permissions, permission):
                            permission_dict[permission] = True
                        else:
                            await ctx.send(f"Invalid permission: {permission}")
                            return
                    permissions = discord.Permissions(**permission_dict)
                except Exception as e:
                    await ctx.send(f"Error parsing permissions: {e}")
                    return

            new_role = await ctx.guild.create_role(name=role_name, colour=color, permissions=permissions)
            await create_role(ctx.guild.id, new_role.id, role_name, color, permissions)
            await ctx.send(f"Created role: {role_name}")

        except discord.Forbidden:
            await ctx.send(f"I don't have the necessary permissions to create roles.")
        except Exception as e:
            await ctx.send(f"An error occurred while creating the role: {e}")

    @commands.command(name="assignrole", help="Assign a role to a user.")
    @commands.has_permissions(manage_roles=True)
    async def assign_role_command(self, ctx, user: discord.Member, role_name: str):
        """
        Handles the !assignrole command, assigning a role to a user.

        Args:
            ctx (commands.Context): The context of the command invocation.
            user (discord.Member): The user to assign the role to.
            role_name (str): The name of the role to assign.

        Returns:
            None
        """
        try:
            role = await get_role_by_name(ctx.guild.id, role_name)
            if not role:
                await ctx.send(f"Role not found: {role_name}")
                return

            await user.add_roles(role)
            await assign_role(user.id, role.id)
            await ctx.send(f"Assigned role {role_name} to {user.mention}")

        except discord.Forbidden:
            await ctx.send(f"I don't have the necessary permissions to assign roles.")
        except Exception as e:
            await ctx.send(f"An error occurred while assigning the role: {e}")

    @commands.command(name="removerole", help="Remove a role from a user.")
    @commands.has_permissions(manage_roles=True)
    async def remove_role_command(self, ctx, user: discord.Member, role_name: str):
        """
        Handles the !removerole command, removing a role from a user.

        Args:
            ctx (commands.Context): The context of the command invocation.
            user (discord.Member): The user to remove the role from.
            role_name (str): The name of the role to remove.

        Returns:
            None
        """
        try:
            role = await get_role_by_name(ctx.guild.id, role_name)
            if not role:
                await ctx.send(f"Role not found: {role_name}")
                return

            await user.remove_roles(role)
            await remove_role(user.id, role.id)
            await ctx.send(f"Removed role {role_name} from {user.mention}")

        except discord.Forbidden:
            await ctx.send(f"I don't have the necessary permissions to remove roles.")
        except Exception as e:
            await ctx.send(f"An error occurred while removing the role: {e}")

    @commands.command(name="roleperms", help="View or modify the permissions of a role.")
    @commands.has_permissions(manage_roles=True)
    async def role_permissions_command(self, ctx, role_name: str, permission: str = None, action: str = None):
        """
        Handles the !roleperms command, allowing for viewing and modifying role permissions.

        Args:
            ctx (commands.Context): The context of the command invocation.
            role_name (str): The name of the role to view or modify permissions for.
            permission (str, optional): The specific permission to modify. Defaults to None.
            action (str, optional): The action to take on the permission (e.g., "add", "remove"). Defaults to None.

        Returns:
            None
        """
        try:
            role = await get_role_by_name(ctx.guild.id, role_name)
            if not role:
                await ctx.send(f"Role not found: {role_name}")
                return

            if permission is None:
                # Display all permissions for the role
                role_perms = await get_role_permissions(role.id)
                permissions_str = "\n".join(f"{perm}: {val}" for perm, val in role_perms.items())
                await ctx.send(f"Permissions for {role_name}:\n{permissions_str}")
                return

            if action is None:
                await ctx.send("Please specify an action ('add' or 'remove').")
                return

            permission = permission.strip().lower()
            if not hasattr(discord.Permissions, permission):
                await ctx.send(f"Invalid permission: {permission}")
                return

            if action.lower() == "add":
                if not role.permissions.has(getattr(discord.Permissions, permission)):
                    # Add the permission
                    role.permissions.update(getattr(discord.Permissions, permission)=True)
                    await update_role_permissions(role.id, permission, True)
                    await ctx.send(f"Added permission {permission} to {role_name}")
                else:
                    await ctx.send(f"Role {role_name} already has permission {permission}")
            elif action.lower() == "remove":
                if role.permissions.has(getattr(discord.Permissions, permission)):
                    # Remove the permission
                    role.permissions.update(getattr(discord.Permissions, permission)=False)
                    await update_role_permissions(role.id, permission, False)
                    await ctx.send(f"Removed permission {permission} from {role_name}")
                else:
                    await ctx.send(f"Role {role_name} does not have permission {permission}")
            else:
                await ctx.send("Invalid action. Please use 'add' or 'remove'.")

        except discord.Forbidden:
            await ctx.send(f"I don't have the necessary permissions to manage role permissions.")
        except Exception as e:
            await ctx.send(f"An error occurred while managing role permissions: {e}")

def setup(bot):
    bot.add_cog(Moderation(bot))