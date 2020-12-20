# coding=utf-8
from __future__ import absolute_import, division, print_function
def create_converted_entity_factory():
    self = None

    def create_converted_entity(ag__, ag_source_map__, ag_module__):

        def tf__train_function(iterator):
            do_return = False
            retval_ = ag__.UndefinedReturnValue()
            with ag__.FunctionScope('train_function', 'fscope', ag__.ConversionOptions(recursive=True, user_requested=True, optional_features=(), internal_convert_user_code=True)) as fscope:
                data = ag__.converted_call(next, (iterator,), None, fscope)
                outputs = ag__.converted_call(self.distribute_strategy.run, (self.train_step,), dict(args=(data,)), fscope)
                outputs = ag__.converted_call(reduce_per_replica, (outputs, self.distribute_strategy), dict(reduction='first'), fscope)
                try:
                    do_return = True
                    retval_ = fscope.mark_return_value(outputs)
                except:
                    do_return = False
                    raise
            (do_return,)
            return ag__.retval(retval_)
        tf__train_function.ag_source_map = ag_source_map__
        tf__train_function.ag_module = ag_module__
        tf__train_function = ag__.autograph_artifact(tf__train_function)
        return tf__train_function
    return create_converted_entity