from leapp.actors import Actor
from leapp.models import SCTPConfig, RpmTransactionTasks
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


def test_scpt_wanted(current_actor_context):
    current_actor_context.feed(SCTPConfig(wanted=True))
    current_actor_context.run()
    assert current_actor_context.consume(RpmTransactionTasks)


def test_scpt_unwanted(current_actor_context):
    current_actor_context.feed(SCTPConfig(wanted=False))
    current_actor_context.run()
    assert not current_actor_context.consume(RpmTransactionTasks)
