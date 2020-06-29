#
# Copyright (c) 2020 Idiap Research Institute, http://www.idiap.ch/
# Written by Angelos Katharopoulos <angelos.katharopoulos@idiap.ch>,
# Apoorv Vyas <avyas@idiap.ch>
#

"""Define the interface that should be implemented by every builder.

Concisely, the interface is simply a parameterless get() method that constructs
the transformer and the ability to set the builder parameters via public
properties.
"""

class BaseTransformerBuilder(object):
    """The builder interface. Simply a get function with no parameters that
    returns a torch.nn.Module."""
    def get(self):
        """Create and return the transformer."""
        raise NotImplementedError()

    @classmethod
    def from_kwargs(cls, **kwargs):
        """Construct a builder and set all the keyword arguments as parameters.

        The keyword argument strict is passed to
        BaseTransformerBuilder.from_dictionary separately.

        See BaseTransformerBuilder.from_dictionary().
        """
        strict = kwargs.pop("strict", True)
        return cls.from_dictionary(kwargs, strict=strict)

    @classmethod
    def from_namespace(cls, args, strict=False):
        """Construct a builder from an argparse Namespace.

        To be used for building transformers from command line arguments.

        See BaseTransformerBuilder.from_dictionary().
        """
        return cls.from_dictionary(vars(args), strict=strict)

    @classmethod
    def from_dictionary(cls, dictionary, strict=True):
        """Construct a builder and set all the parameters in the dictionary.

        Given a dictionary

            d = {"foo": "bar"}

        then

            builder = TransformerEncoderBuilder.from_dictionary(d)

        is equivalent to

            builder = TransformerEncoderBuilder()
            builder.foo = "bar"

        Arguments
        ---------
            dictionary: A dictionary of parameters to set to the builder.
            strict: bool, If a key is not a parameter and strict is set to True
                    then a ValueError is raised, otherwise that dictionary key
                    is ignored (default: True)
        """
        builder = cls()
        for k, v in dictionary.items():
            if not hasattr(builder, k):
                if strict:
                    raise ValueError(("The transformer builder has no "
                                      "parameter {!r}").format(k))
                else:
                    continue
            setattr(builder, k, v)
        return builder
