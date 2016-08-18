from agent import Agent


class ManualAgent(Agent):
    def decide(self, context):
        valid_actions = context.get_valid_actions()
        if len(valid_actions) == 0:
            return None
        while True:
            command = raw_input('Enter a move row, col: ')
            if command == 'quit':
                exit(0)
            elif command == 'show':
                print('Valid moves: {}'.format(valid_actions))
            elif command == 'help':
                print('quit: terminate the match')
                print('help: show this help')
            else:
                try:
                    action = eval(command)
                except Exception as e:
                    print('Invalid input: {}'.format(e))
                if action in valid_actions:
                    return action
                print('Invalid move: {}'.format(action))
