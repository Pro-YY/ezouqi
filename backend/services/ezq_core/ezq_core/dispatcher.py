from ezq_core.accessor import store_event

import ezq_core.handlers as H

async def _noop_handler(*args, **kwargs):
    pass

# event handlers registration
_HANDLERS = {
    'CREATE_ACCOUNT_INIT': H.create_account,
    'UPDATE_ACCOUNT_INIT': H.update_account,
    'UPDATE_ACCOUNT_DONE': _noop_handler,
    'DELETE_ACCOUNT_INIT': H.delete_account,
}

async def dispatch(event, params, *args, **kwargs):
    if event not in _HANDLERS:
        print('handler not found for event: {}'.format(event))
        return
    await store_event(event, params)
    print('# {} [stored] dispatching...'.format(event))
    result = await _HANDLERS[event](params)
    print('# {} [done]'.format(event))
