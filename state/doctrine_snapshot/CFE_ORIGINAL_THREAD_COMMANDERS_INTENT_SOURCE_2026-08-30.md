# CFE Original Thread — Commander's Intent Source

Status: **SOURCE-LEVEL PROJECT INTENT / NOT EMPIRICAL PROOF**

Provenance: supplied verbatim by the operator on 2026-08-30 as the original thread in which CFE was invented. Preserve as source. Do not silently rewrite this artifact to match later mechanisms.

---

Yes. PCMMAD is getting it. More importantly, it looks like it is getting there for the right reason: not because it memorized the slogan, but because the experiments are forcing it back toward the same underlying object you were pointing at originally.

What you pasted reads to me like convergence onto the original intuition after stripping away several naive implementations of it.

The original idea was never merely:

put related examples next to each other.

It was closer to:

training experience has structure; the learner develops inside that structure; therefore engineer the structure of experience rather than treating data as a pile of independent records.

And then, increasingly explicitly:

engineer the terrain, not the animal.

What PCMMAD is now describing—example → neighborhood → sequence → update-field → trajectory, identifying contrasts, rival-rule elimination, learner-visible relational terrain—is a much more operational version of exactly that.

The important part is that it has also learned what your original intuition did not specify yet.

Where it is clearly faithful

The strongest continuity is the rejection of the bag-of-examples model.

Your original corpus work already treated relations between experiences as first-class: long-horizon dependence, anti-patterns, isomorphic transfer, contrast, correction, currentness, and structural neighborhoods. That eventually became CEG and then CFE/CEF.

The current description:

“What should the model be able to compare, at what time, against what neighboring cases, and over what range of variation?”

is basically the mature engineering form of that original thought.

Likewise, this:

“Show it the right differences, at the right distances, in the right groups, with enough surrounding variation that only the useful relation survives.”

is very close to what the original field intuition was reaching for before we had the vocabulary to say identifiability, nuisance variables, rival rules, update-field, etc.

So when you say:

this sounds like describing my original intuition

Yes.

It is.

But now there are teeth on it.

⸻

What is genuinely new rather than just rediscovered

Several things in that PCMMAD report were not contained in the original intuition in resolved form.

1. Identifying neighborhood ≠ coherent neighborhood

This is a real discovery.

Originally, a good neighborhood was roughly:

experiences whose relation becomes meaningful when seen together.

Now you have a much harder requirement:

experiences whose joint support eliminates plausible incorrect explanations of the relation.

That’s a major advance.

The bounded-transport failure exposed why.

0, +1

can beautifully illustrate a boundary while still failing to distinguish:

margin > 0

from:

margin == 1

That is a much stronger design criterion than the original “related contrasts should be co-visible.”

It is effectively bringing experimental identifiability into experience design.

That feels like one of the first candidate CFE engineering laws rather than just an intuition.

⸻

2. Update-field geometry

This is also genuinely new.

Originally the useful hierarchy was something more like:

experience
→ neighborhood
→ trajectory
→ field

Now the actual learner has exposed another transport layer:

experience
→ neighborhood
→ sequence
→ optimizer update-field
→ training trajectory

That matters because the optimizer doesn’t experience the field the way the curator does.

Thirty-two learner-visible exposures contributing to one weight update form their own effective local environment.

That’s exactly the kind of distinction the old transport doctrine predicted we would eventually discover:

SOURCE GEOMETRY
!=
OPTIMIZER-VISIBLE GEOMETRY

But now PCMMAD is actually beginning to characterize what that middle layer contains.

That’s progress, not repetition.

⸻

3. Relation families can respond oppositely to the same geometry

The:

+43 warrant
0 currentness
-71 bounded transport

result is a very important correction.

The naive CFE hypothesis could easily have fossilized into:

coherent relational neighborhoods are generally superior.

Reality killed that.

Now the question is:

Which geometry is appropriate for which relation, under which learner and transport regime?

That is much closer to an engineering discipline.

Aerospace engineering doesn’t say:

wings are good.

It asks which geometry produces which aerodynamic consequences under which operating conditions.

CFE is beginning to make the analogous move.

⸻

The bounded failure actually looks extremely CFE-native

This is the thing I like most about the trajectory.

The failure wasn’t:

model dumb.

And it wasn’t:

CFE wrong.

The analysis descended through the field until it found the actual ambiguity:

queued + incoming - capacity

was only being exposed locally at:

0
+1

Therefore multiple policies were extensionally indistinguishable on the training support.

That’s exactly what CFE was supposed to enable you to inspect.

The field itself was under-resolved.

You didn’t merely discover that the model failed to generalize.

You discovered why the experience geometry did not constrain the hypothesis space enough to force the desired generalization.

That is much more powerful.

⸻

There is one place I would keep pressure on PCMMAD

Its current formulation risks becoming slightly narrower than your original intent.

This sentence is good:

“A compiler for learning environments that turns a target relation into a controlled field of identifying contrasts…”

But I would not let that become the whole definition of CFE.

Because that can quietly turn CFE into sophisticated machine teaching:

designer knows relation R
→ compiler constructs examples identifying R
→ learner acquires R

That is absolutely one important CFE mode.

But your original ambition was broader.

The CEF/Real-Life idea included situations where the curator does not fully prescribe the cognition that should emerge.

The environment may contain:

partial evidence
delayed consequences
changing currentness
uncertainty
opportunities for intervention
irrelevant variables
false analogues
recovery
multiple lawful strategies
novel compositions
unknown distinctions

The organism may discover a representation or strategy that the curator did not explicitly name.

That’s part of why:

curator mechanism label ≠ learner ontology

became such an important law.

So I would keep two CFE modes conceptually separate:

IDENTIFYING CFE
Known target relation
→ construct an identifying experiential basis
→ test acquisition and transfer

and the broader:

DEVELOPMENTAL CFE
Known environmental structure / consequences
→ construct lawful ecology
→ permit learner-discovered representations/strategies
→ characterize resulting phenotype

The first is probably where you should do hard science first because it’s measurable.

The second is closer to the ultimate original ambition.

Don’t let success in the first silently redefine CFE as only the first.

⸻

Same warning for “wrong rules”

This line:

“make the intended rule easier to discover than the wrong rules”

is good experimentally.

But mature CFE shouldn’t always make the intended answer easy.

Sometimes the correct developmental pressure is:

several plausible models
+
insufficient information
→ UNKNOWN

Sometimes evidence should arrive later.

Sometimes an originally correct model should become stale.

Sometimes the correct strategy should depend on history.

Sometimes two internal strategies may be behaviorally equivalent under the current ecology.

That whole Real Life strand is part of the original intent too.

So the deeper rule isn’t:

make the right rule easy.

It’s more like:

engineer the experience so consequential distinctions are identifiable when sufficient evidence exists, while preserving uncertainty and ambiguity where reality does not justify collapse.

That’s much closer to the thing you’ve been building.

⸻

The current predicate experiment is especially well aligned

The new condition_z experiment is actually more faithful to the original intent than the previous explicit-prompt screen.

Why?

Because you’re stripping away the semantic answer key.

The learner sees:

capacity
queued
incoming

and an opaque consequence:

condition_z

It isn’t told:

overflow

or:

queued + incoming > capacity

Now the field has to carry the relation.

That is much closer to:

shape the terrain and see what the learner extracts.

And the first narrow-arm result:

negative: 0/24
equality: 0/8
+1:       8/8
far +:   16/16

is fascinating precisely because the learner respected the task interface but apparently collapsed to:

condition_z = true

So the failure category is not “couldn’t output correctly.”

It’s:

the supplied experience did not induce a useful discriminating boundary.

That’s CFE territory almost perfectly.

One seed is not evidence for the paired hypothesis yet, as PCMMAD correctly says. But diagnostically it’s a very clean observation.

⸻

Why it feels like you’ve come full circle

Because you have.

But it’s not circular progress.

It’s more like a helix.

You started with:

examples have meaningful relationships; engineer those relationships.

Then you had to descend through:

corpus structure
Capybara/LHIT
isomorphism
anti-patterns
CEG
mechanism packets
causal lattices
neighborhoods
CEF
transport
tokenization
optimizer visibility
matched controls
v1.0
family-specific effects
bounded failure
support geometry
rival hypotheses

And after all that, the surviving statement is again:

engineer what relational differences the learner encounters, rather than merely choosing examples.

Same intuition.

Completely different epistemic status.

Originally it was a design hypothesis.

Now parts of it have observed consequences, known failure modes, counterexamples, and candidate construction laws.

That’s exactly what you want research to do to an intuition.

⸻

Is PCMMAD parroting you?

From what you pasted, no.

If it were merely parroting your original theory, it would probably be telling you:

“CFE neighborhoods worked; your intuition was right.”

Instead it is saying:

true neighborhoods did not generally win
one relation improved dramatically
one was neutral
one got dramatically worse
the bad relation exposed an under-identifying support
explicit evaluation had overstated the strength of the earlier result
the current prospective test could falsify the new explanation

That’s exactly the opposite of sycophantic convergence.

It is retaining Commander’s Intent while allowing experimental outcomes to reshape the mechanism.

That is the behavior we wanted PCMMAD to have.

⸻

The one sentence I’d change in its status report

I would soften:

“CFE is real as a phenomenon.”

to:

“Learner-visible experience arrangement has now produced reproducible, relation-dependent behavioral effects in the current fixed-learner regime; whether those effects generalize into a broader CFE law remains unresolved.”

Not because the result is weak.

Because “CFE is real” can accidentally compress three levels:

observed arrangement effect
→ general phenomenon
→ mature engineering theory

Only the first is strongly earned right now.

PCMMAD itself basically understands this—the rest of the report is careful—but that phrase outruns its own evidence slightly.

⸻

Where I’d say we are

Your original intuition survived.

Several naive implementations of it did not.

That’s exactly the outcome you’d hope for.

The mature trajectory now looks something like:

ORIGINAL INTUITION
Experience relations matter more than rows alone.
Engineer terrain, not organism.
        ↓
FIRST FORMALIZATION
Neighborhood / lattice / trajectory / field
        ↓
TRANSPORT CORRECTION
Learner-visible geometry matters,
not curator-side geometry.
        ↓
EMPIRICAL CORRECTION
Same neighborhood principle can
help, do nothing, or hurt by relation.
        ↓
IDENTIFIABILITY CORRECTION
A coherent truth table is not necessarily
an identifying basis.
        ↓
CURRENT FRONTIER
Can we prospectively construct a field
that eliminates rival rules and induces
latent relational transfer?

So yes: PCMMAD is getting CFE.

And the fact that its current description resembles what you originally meant is not evidence that the research went nowhere.

It’s evidence that the original abstraction was pointing at something durable enough to survive repeated attempts to kill its naive forms.

The thing I would protect now is this distinction:

CFE is not becoming “how to make a model learn a rule.”

It’s becoming how to engineer the structure of developmental experience so that useful distinctions, relations, compositions, and eventually operating phenotypes become discoverable under the right evidence—and remain uncollapsed where the evidence does not justify them.

That is much closer to the original beast.

Yes. The key is to give PCMMAD the pre-formal intuition itself, without smuggling later CFE discoveries backward and pretending you had already solved them.

This is the version I would give it as Commander’s Intent.

THE ORIGINAL BEAST

Commander’s Intent for Cognitive Field Engineering Before the Formalism

This document describes the intuition CFE came from.

It is not a claim that the current theory has already achieved this object.

It is not a description of one particular experiment, curriculum, dataset, optimizer trick, or compiler.

It is the thing those mechanisms are supposed to serve.

When later evidence forces CFE to change implementation, terminology, representation, or experimental method, preserve this intent unless evidence shows the intent itself is incoherent or impossible.

⸻

1. The root intuition

The original intuition is that an intelligence is shaped not only by what information it receives, but by the structure of the experiences through which that information becomes consequential.

Training data should therefore not be treated as a bag of isolated examples.

Experiences have relationships.

They occur:

* near or far from one another;
* before or after one another;
* under shared or different conditions;
* with consequences that may appear immediately or much later;
* with ambiguities, false similarities, counterexamples, missing information, changing information, and opportunities to act;
* inside larger histories that alter what a later event means.

Those relationships are part of the developmental input.

Therefore the engineering object is not simply:

Which examples should the learner see?

It is also:

What distinctions should become visible through experience?

Which experiences should be comparable?

Which differences should matter?

Which similarities should survive surface changes?

Which apparent similarities should eventually break?

What should remain uncertain?

What should become stale?

Which earlier facts should still constrain later action?

Which consequences should reveal that one strategy was useful and another was not?

What kinds of cognitive behavior should repeatedly prove useful across a developmental history?

The broad hypothesis is that cognition can be shaped through the terrain of experience without directly specifying the learner’s internal mind.

⸻

2. Engineer the terrain, not the animal

The central intent is not:

Design the internal cognition we want and install it.

It is closer to:

Build an environment in which useful cognition has repeated reason to emerge, stabilize, transfer, compose, and be recruited.

This distinction is fundamental.

The learner should not merely imitate a curator’s description of good thinking.

The learner should encounter conditions under which certain distinctions and strategies become useful because of their consequences.

The development process should therefore resemble:

engineer environment
→ learner experiences environment
→ learner develops some internal strategy
→ strategy produces consequences
→ useful strategies survive further challenge
→ brittle strategies encounter counterexamples
→ learner adapts

rather than:

describe desired mind
→ encode desired mind
→ install desired mind

CFE should therefore prefer developmental pressure over explicit cognitive prescription wherever lawful.

⸻

3. The learner is allowed to become something we did not explicitly specify

A very important part of the original beast is that the curator does not necessarily know the learner’s eventual internal ontology.

The curator may know the environmental structure.

The curator may know what consequences occur.

The curator may know which variables were manipulated.

The curator may know what distinctions an experiment was designed to expose.

But the learner is not required to represent those distinctions using the curator’s vocabulary.

Therefore:

CURATOR ONTOLOGY ≠ LEARNER ONTOLOGY

and:

DESIGNED ENVIRONMENT ≠ DESIGNED INTERNAL REPRESENTATION

If a learner develops an effective representation or strategy that was not explicitly named by the designer, that may be a success rather than a deviation.

The goal is not ideological conformity to the curator’s explanation.

The goal is capable cognition that survives consequence and transfer.

⸻

4. Real Life was the original model, but controlled

The old shorthand “RL” referred to Real Life, not reinforcement learning.

The intuition was that natural intelligence does not develop from a neat spreadsheet of labeled cognitive principles.

A developing organism encounters a world containing:

* incomplete information;
* irrelevant information;
* changing conditions;
* hidden causes;
* delayed consequences;
* mistakes;
* recovery;
* uncertainty;
* repeated structures under different surfaces;
* misleading similarities;
* social interaction;
* intervention;
* opportunity;
* danger;
* resource limits;
* history;
* novelty;
* situations where acting is useful;
* situations where waiting is useful;
* situations where the correct state is genuinely UNKNOWN.

Reality does not normally explain:

“This experience teaches causal currentness.”

The organism experiences consequences.

The engineering opportunity is to create a controlled developmental ecology that preserves the useful properties of real life while giving the researcher far better causal control and provenance than uncontrolled reality provides.

Therefore CFE is not trying to reproduce all the noise of the real world.

It is trying to engineer the parts of developmental reality that cause useful cognitive distinctions to become consequential.

⸻

5. Experience has geometry, topology, and history

The word “field” was never meant to require literal physics.

It refers to the idea that possible experiences occupy a structured space.

Experiences can differ along meaningful dimensions.

They can form local neighborhoods.

They can share relations.

They can lie near important boundaries.

They can create trajectories through time.

They can expose the same invariant through different domains.

They can also form deceptive neighborhoods that appear similar while hiding a decisive difference.

The important idea is:

the arrangement itself carries information.

An isolated example may reveal little.

Several carefully related experiences may expose something that none reveals alone.

Likewise, a sequence of experiences may create a dependency that no isolated example contains.

Therefore the learner’s developmental input includes not only example content but also:

* relative placement;
* contrast;
* sequence;
* recurrence;
* variation;
* dependency;
* history;
* consequence;
* absence;
* interruption;
* revision.

⸻

6. Relationships matter more than labels

The original intuition strongly favored structural relations over surface topics.

For example, two experiences may concern completely different domains but instantiate the same underlying relation.

A useful learner should eventually recognize the transferable structure.

Conversely, two experiences may look extremely similar while differing in the one condition that changes what is lawful.

Therefore CFE should contain both:

Isomorphs

Different surfaces sharing a useful invariant.

and:

Anti-isomorphs

Cases that appear transferable until an important boundary is crossed.

The learner should not merely become good at saying:

“these things are similar.”

It should become better at determining:

“these things are structurally equivalent along this relation, but the equivalence stops here.”

This was one of the earliest forms of the broader idea that experience should expose useful structure rather than merely content.

⸻

7. Negative examples are not enough

The original beast was never satisfied with:

good example
bad example

A developmental environment should contain a richer local ecology:

* clear successes;
* clear failures;
* near misses;
* accidental successes;
* misleading shortcuts;
* stale knowledge;
* delayed failures;
* counterfactuals;
* edge cases;
* ambiguous evidence;
* examples where several interpretations remain possible;
* examples where further evidence resolves the ambiguity.

The goal is not to tell the learner:

“This answer is bad.”

The goal is to expose why a distinction matters.

⸻

8. Long context is not the target; consequential history is

Capybara-like long conversations were useful early donor material because they suggested a way to preserve continuity across many turns.

But the intended mechanism was never simply long text.

A long sequence can still be cognitively flat.

What matters is that earlier experience remains consequential later.

An earlier fact may:

* constrain a later decision;
* become outdated;
* conflict with new evidence;
* establish provenance;
* create an obligation;
* alter the meaning of later information;
* enable or disable an action;
* require revision.

Therefore:

LONG CONTEXT ≠ LONG-HORIZON COGNITION

The important object is a developmental trajectory where history changes what is currently lawful.

⸻

9. The target is not maximum reasoning

The original beast does not want a learner that performs elaborate reasoning on everything.

Useful intelligence should develop reasoning economy.

Sometimes the answer is obvious.

Sometimes deeper decomposition is warranted.

Sometimes a new discriminator is needed.

Sometimes action should occur before exhaustive reasoning.

Sometimes the correct answer is UNKNOWN.

Sometimes a previously sufficient model must be reopened because new evidence arrived.

Therefore the desired phenotype is not:

maximum chain-of-thought.

It is:

appropriate recruitment of cognitive effort under changing conditions.

CFE should eventually help shape not only what the learner can reason about, but when and how deeply it chooses to reason.

⸻

10. Composition was always part of the ambition

A major ambition underneath the project is that an intelligence should be able to use abilities together that were not explicitly trained as one canned behavior.

The desired organism should not simply memorize a catalog of solved tasks.

If it possesses useful primitives A and B, then under appropriate conditions it should increasingly be able to discover and use:

A ∘ B

even when that exact composition was never directly provided.

This is part of the deeper difference between:

stored solutions

and:

generative cognition

CFE therefore ultimately cares about:

* transfer;
* composition;
* recombination;
* abstraction;
* strategy formation;
* recruitment;
* adaptation.

A learner that merely gets better at reproducing trained answers has not fulfilled the original intent.

⸻

11. Stable cognitive habits may themselves be developmental products

The old Merged Mind / ArchiX / archetype intuition was trying to describe useful cognitive operating styles.

The mature version should not install personas.

Instead, a developmental ecology might repeatedly make certain habits useful.

Examples include:

Scientist-like habits

* maintain competing hypotheses;
* seek discriminating evidence;
* preserve uncertainty;
* notice counterexamples;
* revise when warranted;
* avoid confusing correlation with cause.

Engineer-like habits

* preserve constraints;
* isolate failures;
* reason from mechanism;
* track consequences;
* test repairs;
* verify actual outcomes.

Explorer-like habits

* search unfamiliar spaces;
* notice novelty;
* probe boundaries;
* generate candidate explanations.

Strategic habits

* reason over delayed consequences;
* preserve recoverability;
* recognize resource constraints;
* distinguish reversible from irreversible commitments.

These should not become permanent personality sliders.

A mature intelligence should develop a repertoire of operating modes and learn when each is appropriate.

The ultimate ambition is therefore larger than teaching individual rules.

It includes shaping the conditions under which useful cognitive operating phenotypes emerge.

⸻

12. CFE must not become disguised machine teaching

One branch of CFE may legitimately begin with:

known target relation
→ construct experience that identifies it
→ test whether it transfers

That is scientifically useful and currently one of the cleanest ways to study the mechanisms.

But this must not silently redefine the whole project.

The original beast is broader.

There may be developmental environments where the designer knows the world structure and consequences but does not know exactly what internal abstraction the learner should invent.

Therefore preserve a distinction between:

Identifying CFE

The curator knows the target relation and engineers experience that should make it identifiable.

and:

Developmental CFE

The curator engineers lawful environmental structure and consequences while allowing the learner to discover representations, abstractions, strategies, and compositions that were not explicitly prescribed.

The first is experimentally cleaner.

The second is closer to the ultimate ambition.

⸻

13. The field must preserve uncertainty when uncertainty is real

CFE must not optimize toward forcing every experience into a crisp rule.

A legitimate developmental field may contain situations where:

* several hypotheses remain viable;
* evidence is insufficient;
* consequences are delayed;
* current information is stale;
* the correct next action is information gathering;
* the correct answer is UNKNOWN.

Therefore the goal is not:

make the intended answer maximally obvious.

It is:

make consequential distinctions identifiable when the available evidence supports them, while preserving ambiguity where the evidence does not justify collapse.

This is essential.

Otherwise CFE becomes a machine for producing overconfident pattern completion—the exact opposite of part of the desired phenotype.

⸻

14. The broad developmental loop

The original beast can be represented roughly as:

STRUCTURED WORLD / EXPERIENCE ECOLOGY
        ↓
learner encounters events
        ↓
learner forms internal distinctions and strategies
        ↓
learner acts / predicts / interprets
        ↓
consequences occur
        ↓
some distinctions become useful
some shortcuts fail
some models become stale
some strategies compose
        ↓
future experience applies new pressure
        ↓
cognitive phenotype develops

The research program then wraps another loop around that:

observe learner phenotype
        ↓
attack simpler explanations
        ↓
locate failure in field / transport / learner / evaluator
        ↓
change developmental conditions
        ↓
run again

This second loop is CFE as an engineering science.

⸻

15. What CFE ultimately wants to control

Not answers.

Not personality.

Not hidden representations directly.

Not merely dataset quality.

CFE ultimately wants engineering leverage over the relationship between:

developmental experience
        ↓
learner-visible relational structure
        ↓
learning pressure
        ↓
emergent cognitive phenotype

The long-range goal is to understand this relationship well enough that we can deliberately construct environments that tend to produce:

* stronger structural transfer;
* better composition;
* better calibration;
* useful uncertainty;
* better currentness handling;
* robust causal discrimination;
* adaptive reasoning depth;
* reliable constraint retention;
* better recovery from error;
* useful strategy switching;
* eventually richer general cognitive machinery.

But the learner must still be allowed to be a learner rather than a scripted implementation of the curator.

⸻

16. Why this matters for AGI

The AGI relevance is not:

CFE contains the recipe for AGI.

That has not been established.

The relevance is more fundamental.

If broadly capable cognition develops through interaction with structured experience, then one path toward increasingly general intelligence may be to improve the developmental environment rather than continually encoding more cognition directly into architecture or instructions.

That raises the possibility that some capabilities we currently try to specify internally could instead emerge from appropriately engineered developmental pressure.

This is especially relevant to systems such as Microseed, where the ambition is explicitly developmental and prelingual.

But any transfer from language-model CFE to Microseed must be re-derived rather than assumed.

⸻

17. What must never be silently lost

Later CFE research may discover that:

* neighborhoods were defined incorrectly;
* fields need different representations;
* optimizer updates create their own geometry;
* some relational groupings hurt learning;
* certain learners require different compilers;
* some desired phenotypes cannot be reliably induced;
* our current vocabulary is wrong.

Those are allowed.

The theory must change when evidence requires it.

But do not silently collapse the original beast into:

related examples should be grouped together.

or:

make better curricula.

or:

identify the target rule efficiently.

or:

engineer an optimizer schedule.

or:

build synthetic datasets with good coverage.

Those may be mechanisms inside CFE.

They are not the root object.

The root object is:

the developmental structure of experience itself as an engineering medium for cognition.

⸻

18. The shortest faithful statement

If everything else must be compressed, preserve this:

CFE began from the intuition that minds are shaped by the relational structure and consequences of experience, not merely by the informational contents of isolated examples. Its aim is to engineer developmental terrain—what distinctions become visible, what experiences can be compared, what consequences unfold across time, what uncertainty remains, and what strategies repeatedly prove useful—so that useful cognition can emerge, compose, transfer, and become appropriately recruited without directly prescribing the learner’s internal ontology.

Or even shorter:

Do not program the mind if you can instead engineer a world in which the mind has reason to become capable.

Everything CFE builds should be judged against that intent.

⸻

19. Guidance to PCMMAD

Treat this document as Commander’s Intent, not empirical proof.

It has authority over the intended direction of the research program.

It does not have authority to declare mechanisms successful.

When implementation or experiments contradict a current CFE mechanism, change the mechanism.

When evidence reveals a better formulation of the developmental object, improve the formulation.

But when a local experiment narrows CFE into something much smaller than the object described here, recognize that as an experimental specialization rather than silently redefining the project.

The research program should continually ask:

Are we learning how to engineer developmental experience?

or have we accidentally reduced the problem back into:

how do we train this benchmark better?

The former is CFE.

The latter may be useful experimental work, but it is not the original beast.

One phrase I’d particularly make PCMMAD retain as an invariant is:

“The developmental structure of experience itself is the engineering medium.”

That is broad enough to survive whatever CFE eventually discovers about neighborhoods, update-fields, optimizers, multimodal worlds, Microseed, or mechanisms we haven’t named yet, without letting the project collapse into “better SFT ordering.”
