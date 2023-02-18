thank_you_embed =
    .title = Obrigado por me escolher!
    .description = 
    Olá, eu sou o Gatekeeper, um bot anti bot!

    Você precisa configurar algumas coisas antes que eu possa começar a pegar esses bots danadinhos.
    Use o comando /setup e siga as instruções.

setup_cancel_button = Cancelar
    .pressed = A configuração foi cancelada.

setup_continue_button = Continuar
setup_retry_button = Tentar novamente


setup_intro_embed =
    .title = Bem-vindo as configuraçãoes iniciais!
    .description =
    Para que o bot possa começar a funcionar no seu servidor, precisamos configurar algumas coisinhas.

    O processo é bem simples, possui somente 3 passos.
    .step_1_name = Passo 1
    .step_1_value = Verificaremos se o bot possui todas as permissões necessárias.
    .step_2_name = Passo 2
    .step_2_value = Selecione um canal para histórico de entradas e saídas.
    .step_3_name = Passo 3
    .step_3_value = Selecione qual convite será utilizado.
    .footer = Clique em "Continuar" para começar.

setup_permissions_embed =
    .title = Verificando permissões.
    .description_missing_permissions =
    O bot precisa das seguintes permissões para funcionar corretamente no seu servidor, mas parece que ele não possui todas elas.

    { $permissions }

    Certifique-se de que o bot tenha todas as permissões listadas acima e clique em "Tentar novamente".
    .description_has_permissions = O bot tem todas as permissões necessárias!

    { $permissions }

    .footer_missing_permissions = Clique em "Tentar novamente" para tentar novamente.
    .footer_has_permissions = Clique em "Continuar" para continuar.

setup_cancel_button_pressed = A configuração foi cancelada.

permissions = Permissões
    .kick_members = Expulsar membros
    .create_instant_invite = Criar convite instantâneo
    .manage_webhooks = Gerenciar webhooks
    .read_messages = Ver canais
    .send_messages = Enviar mensagens
    .send_messages_in_threads = Enviar mensagens em tópicos
    .use_external_emojis = Usar emojis externos
    .add_reactions = Adicionar reações
