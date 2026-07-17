from dataclasses import dataclass 
from typing import Set,List, Optional

@dataclass
class ATSNode:
    pass

@dataclass
class CharNode(ATSNode):
    char:str

    def __repr__(self):
        return f"{self.char!r}"

@dataclass
class DotNode(ATSNode):
    def __repr__(self):
        return "Dot(.)"
    
@dataclass
class CharClassNode(ATSNode):  #[^abc] some thing like this 
    chars:Set[str]
    negated:bool = False

    def __repr__(self):
        prefix = "^" if self.negated else ""
        return f"CharClass([{prefix}{self.chars}])"

@dataclass
class PredefinedClassNode(ATSNode): 
    class_type:str # d , D , w , W , s , S

    def __repr__(self):
        return f"PredefinedClass(\\{self.class_type})"


@dataclass
class QuantifiedNode(ATSNode):  
# ex: a* tree look like this so that why we need a child node 
# *
# |
# a
    child: ATSNode
    
    min_count:int  # {min,max} min is required not optional here 
    max_count:Optional[int] # max is optional why because example a{1,} this means max is unlimited
    greedy:bool = True # to identify lazy or not (*? , ?? ,+? ,{}?)



    def __repr__(self):
        if self.min_count == 0 and self.max_count == 1:
            q = "?" if self.greedy  else "??"
        elif self.min_count == 0 and self.max_count is None:
            q = "*" if self.greedy else "*?"
        elif self.min_count == 1 and self.max_count is None:
            q = "+" if self.greedy else "+?"
        else:
            q = f"{{{self.min_count},{self.max_count}}}"
            if not self.greedy:
                q +="?"
        return f"Quantifier({self.child} {q} )"


@dataclass
class ConcatNode(ATSNode):
    childern:List[ATSNode]


    def __repr__(self):
        return f"Concat({self.childern})"


@dataclass
class AlternationNode(ATSNode):
    alternatives:List[ATSNode]

    def __repr__(self):
        return f"Alternation({self.alternatives})"


@dataclass
class GroupNode(ATSNode):
    child:ATSNode # why here iam single node inside group has a concat node ex:- (ab) a and b will connect to the concat node right
    group_number:int # this will help us to refernece of the group 

    def __repr__(self):
        return f"Group#{self.group_number}({self.child})"


@dataclass
class NonCapturingGroupNode(ATSNode):
    child:ATSNode # here not use group number because non capture group (?:)

    def __repr__(self):
        return f"NonCapturingGroup({self.child})"

@dataclass
class BackrefernceNode(ATSNode):
    group_number:int


    def __repr__(self):
        return f"Backrefernce(\\{self.group_number})"


@dataclass
class AnchorNode(ATSNode):
    anchor_type:str # '^', '$', 'b', 'B'

    def __repr__(self):
        symbols = {"^":"^","$":"$","b":r"\b","B":r"\B"}
        return f"Anchor({symbols.get(self.anchor_type,self.anchor_type)})"
    



@dataclass
class LookaheadNode(ATSNode):
    # like as concat node right but here not consuming like telescope just see that sit  ex: viay(?=kumar.+) here kumar and .+ combine with concat node that's why need child
    child:ATSNode
    postive:bool = True #(?=) for +ve and -ve is (?!)

    def __repr__(self):
        prefix = "?=" if self.postive else "?!"
        return f"Lookahead({prefix}{self.child})"
    
@dataclass
class LookbehindNode(ATSNode):
    #here same like as lookaheadnode 
    child:ATSNode
    positive:bool = True

    def __repr__(self):
        prefix = "?<=" if self.positive else "?<!"
        return f"Lookbehind({prefix}{self.child})"
    


            