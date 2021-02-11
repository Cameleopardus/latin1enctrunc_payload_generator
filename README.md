# latin1enctrunc_payload_generator
    Some applications including older versions of Node will improperly convert unicode characters into latin1 encoding
    by truncating the unicode values to fit into the 0-95 character space for basic latin characters. 
    This script takes a text body in latin characters and returns unicode characters
    that when converted by a vulnerable application would translate back into the original basic latin text body.

    This is useful for performing http request smuggling and server side request forgery.