thank_you_embed =
    .title = "Thank you for choosing me!"
    .description =
    "Hello, I am the Gatekeeper, an anti bot bot!

    To start, you need to set up some things before I can start catching those pesky bots.
    Use the /setup command and follow the instructions."

setup_cancel_button = Cancel
    .pressed = The setup has been stopped.

setup_continue_button = Continue
setup_retry_button = Retry

setup_intro_embed =
    .title = Welcome to the initial setup!
    .description =
    For the bot to start working on your guild, we need to configure some things.

    The process is simple, it only has 3 steps.
    .step_1_name = Step 1
    .step_1_value = We will check if the bot has all the necessary permissions.
    .step_2_name = Step 2
    .step_2_value = Select a channel for entry and exit logs.
    .step_3_name = Step 3
    .step_3_value = Select which invite will be used.
    .footer = Click "Continue" to start.

setup_permissions_embed =
    .title = Checking permissions
    .description_missing_permissions =
    The bot needs the following permissions to work properly on your guild but it seems that it does not have all of them.

    { $permissions }

    Make sure that the bot has all the permissions listed above and then click in "Retry".
    .description_has_permissions = The bot has all the necessary permissions!

    { $permissions }

    .footer_missing_permissions = Click "Retry" to retry.
    .footer_has_permissions = Click "Continue" to continue.

setup_log_view =
    .title = Select a channel for entry and exit logs
    .description =
    Setting up a channel for entry and exit logs is optional, but __highly recommended__.
    Every time a user joins or leaves the guild, a message will be sent to the selected channel.
    This includes users who are kicked by the JoinGuard verification system, along with useful information about the user.

    We recommend using a dedicated channel for logs, such as #logs, and ensuring that only your staff have access to it.

    If you choose not to set up a log channel, you can click "Skip" to move on to the next step.
    .description_missing_permissions = 
    The bot does not have the Manage Webhooks permission, which is required to create the webhook that will be used to send the logs.
    Please ensure that the bot has the Manage Webhooks permission for the selected channel and then click "Retry" to try again.

    .footer_missing_permissions = Click "Retry" to retry or click "Skip" to skip this step.
    .footer = Select a channel or click "Skip" to skip this step.
    .placeholder = Select a channel for the logs.
    .channel_selected = The channel { $channel } has been selected.

setup_invite_view = 
    .title = Select an invite for the Join Guard
    .description =
    The Join Guard is a verification system designed to prevent potential self-bots from joining your guild. Upon joining, each user will be checked against certain requirements.
    If they do not meet the requirements, the bot will send them a message asking them to complete a verification process and then kick them from the guild.
    Once the user successfully completes the verification process, they will be redirected back to the guild using a selected invite.
    .info_vanity_invite = You can choose to use the guild's existing vanity invite ({ $invite_url }) or generate a new invite to be used by the Join Guard.
    .info_normal_invite = As the guild does not have a vanity invite, the bot will need to generate a new invite to be used by the Join Guard.

    .footer_vanity_invite = Click "Use vanity invite" to use the guild's vanity invite or click "Generate new invite" to generate a new invite.
    .footer_normal_invite = Click "Generate new invite" to generate a new invite.

    .vanity_invite_button = Use vanity invite
    .generate_invite_button = Generate new invite

    .error_no_vanity_invite = This guild doesn't have a vanity invite.


permissions = Permissions
    .kick_members = Kick members
    .create_instant_invite = Create instant invite
    .manage_webhooks = Manage webhooks
    .read_messages = Read messages
    .send_messages = Send messages
    .send_messages_in_threads = Send messages in threads
    .use_external_emojis = Use external emojis
    .add_reactions = Add reactions