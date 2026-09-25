# Glossary

Every term the course uses, defined in one plain sentence. Keep this open in a second tab
while you read. Terms are grouped roughly by theme, and the search box at the top of the
site will jump you straight to any of them.

!!! tip
    On a first encounter, a one-line definition is enough to keep reading. The full
    explanation always lives in the chapter where the term is introduced.

## Core AI and ML terms

<dl class="caisp-terms" markdown>

<dt>Artificial Intelligence (AI)</dt>
<dd>The broad field of building computer systems that perform tasks we associate with human
intelligence, such as understanding language or recognising images.</dd>

<dt>Machine Learning (ML)</dt>
<dd>A subset of AI where a system learns patterns from data instead of being explicitly
programmed with rules.</dd>

<dt>Deep Learning</dt>
<dd>A subset of ML that uses neural networks with many layers, which excel at learning from
large, unstructured data like text, images, and audio.</dd>

<dt>Model</dt>
<dd>The output of a training process: a file (really, a big collection of numbers) that can
take an input and produce a prediction or generation.</dd>

<dt>Algorithm</dt>
<dd>The procedure used to train or run a model; the recipe, as opposed to the model, which
is the cake.</dd>

<dt>Training</dt>
<dd>The process of adjusting a model's internal numbers so its outputs match the patterns in
a dataset.</dd>

<dt>Inference</dt>
<dd>Using an already-trained model to produce an output for a new input; what happens every
time you send a chatbot a message.</dd>

<dt>Dataset</dt>
<dd>The collection of examples a model learns from.</dd>

<dt>Parameter (weight)</dt>
<dd>One of the many numbers inside a model that get tuned during training; large models have
billions of them.</dd>

<dt>Narrow AI</dt>
<dd>AI that is good at one specific task (all AI that exists today is narrow AI).</dd>

<dt>General AI (AGI)</dt>
<dd>Hypothetical AI that could perform any intellectual task a human can; it does not exist
yet.</dd>

</dl>

## Learning approaches

<dl class="caisp-terms" markdown>

<dt>Supervised learning</dt>
<dd>Training on labelled examples, where each input comes with the correct answer.</dd>

<dt>Unsupervised learning</dt>
<dd>Training on unlabelled data, letting the model find structure or groupings on its
own.</dd>

<dt>Reinforcement learning</dt>
<dd>Training an agent to make decisions by rewarding good outcomes and penalising bad
ones.</dd>

<dt>Fine-tuning</dt>
<dd>Taking a pre-trained model and training it a little more on a narrower dataset to
specialise it.</dd>

</dl>

## Language model terms

<dl class="caisp-terms" markdown>

<dt>Large Language Model (LLM)</dt>
<dd>A model trained on vast amounts of text that predicts likely next words, enabling it to
generate and understand language.</dd>

<dt>Token</dt>
<dd>A chunk of text (a word, part of a word, or punctuation) that a language model reads and
writes; models think in tokens, not letters.</dd>

<dt>Tokenizer</dt>
<dd>The component that splits text into tokens and converts them to numbers for the model
(and back again).</dd>

<dt>Embedding</dt>
<dd>A list of numbers (a vector) representing the meaning of a piece of text, so that similar
meanings have similar vectors.</dd>

<dt>Transformer</dt>
<dd>The neural-network architecture behind modern LLMs, built around an "attention"
mechanism that weighs how much each word relates to the others.</dd>

<dt>GPT</dt>
<dd>Generative Pre-trained Transformer; a family of transformer models designed to generate
text.</dd>

<dt>BERT</dt>
<dd>Bidirectional Encoder Representations from Transformers; a transformer model designed to
understand text rather than generate long passages.</dd>

<dt>Foundational (base) model</dt>
<dd>A large model trained on broad data, intended to be adapted (via fine-tuning or
prompting) to many downstream tasks.</dd>

<dt>Prompt</dt>
<dd>The text input you give an LLM to get a response.</dd>

<dt>System prompt</dt>
<dd>Hidden instructions the application gives the model to shape its behaviour, separate from
what the user types.</dd>

<dt>Context window</dt>
<dd>The maximum amount of text (in tokens) a model can consider at once.</dd>

<dt>Hallucination</dt>
<dd>When a model produces confident output that is factually wrong or fabricated.</dd>

<dt>Retrieval Augmented Generation (RAG)</dt>
<dd>A technique that fetches relevant documents and feeds them to an LLM so its answers are
grounded in real, current data.</dd>

<dt>Vector database</dt>
<dd>A database that stores embeddings and finds the ones most similar to a query; the memory
behind most RAG systems.</dd>

</dl>

## Security terms

<dl class="caisp-terms" markdown>

<dt>Attack surface</dt>
<dd>The total set of points where an attacker could try to get in or cause harm.</dd>

<dt>Threat</dt>
<dd>A potential event that could harm a system.</dd>

<dt>Vulnerability</dt>
<dd>A weakness that a threat could exploit.</dd>

<dt>Exploit</dt>
<dd>A concrete method or piece of code that takes advantage of a vulnerability.</dd>

<dt>Mitigation</dt>
<dd>A measure that reduces the likelihood or impact of a threat.</dd>

<dt>Asset</dt>
<dd>Anything valuable enough to protect: data, a model, a reputation, a service.</dd>

<dt>Trust boundary</dt>
<dd>A line in a system where data crosses from a less-trusted zone into a more-trusted one,
and therefore must be checked.</dd>

<dt>Threat modeling</dt>
<dd>A structured process for finding, rating, and addressing threats before they are
exploited.</dd>

<dt>STRIDE</dt>
<dd>A checklist of six threat categories: Spoofing, Tampering, Repudiation, Information
disclosure, Denial of service, and Elevation of privilege.</dd>

<dt>Prompt injection</dt>
<dd>An attack that smuggles instructions into an LLM's input to override its intended
behaviour.</dd>

<dt>Data poisoning</dt>
<dd>Corrupting a model's training data so it learns attacker-chosen behaviour.</dd>

<dt>Model theft</dt>
<dd>Stealing a model's weights or reconstructing its behaviour without authorisation.</dd>

<dt>Backdoor</dt>
<dd>Hidden behaviour planted in a model that activates on a secret trigger.</dd>

<dt>Supply chain attack</dt>
<dd>Compromising a system by tampering with something it depends on, such as a library or a
downloaded model.</dd>

</dl>

## Frameworks and organisations

<dl class="caisp-terms" markdown>

<dt>OWASP</dt>
<dd>The Open Worldwide Application Security Project; publishes the widely-used "Top 10" lists,
including one for LLM applications.</dd>

<dt>MITRE ATT&CK</dt>
<dd>A knowledge base of real-world attacker tactics and techniques for traditional
systems.</dd>

<dt>MITRE ATLAS</dt>
<dd>The AI-focused counterpart to ATT&CK, cataloguing tactics and techniques against machine
learning systems.</dd>

<dt>NIST AI RMF</dt>
<dd>The US National Institute of Standards and Technology's AI Risk Management
Framework.</dd>

<dt>ISO/IEC 42001</dt>
<dd>An international standard for managing AI responsibly within an organisation.</dd>

<dt>EU AI Act</dt>
<dd>The European Union's comprehensive law regulating AI systems by risk level.</dd>

<dt>SBOM</dt>
<dd>Software Bill of Materials; a complete inventory of the components that make up a piece
of software.</dd>

<dt>SLSA</dt>
<dd>Supply-chain Levels for Software Artifacts; a framework for securing how software is
built and delivered.</dd>

</dl>

## DevOps and tooling

<dl class="caisp-terms" markdown>

<dt>DevOps</dt>
<dd>A set of practices that combine software development and IT operations to ship software
faster and more reliably.</dd>

<dt>DevSecOps</dt>
<dd>DevOps with security built into every stage rather than bolted on at the end.</dd>

<dt>CI/CD Pipeline</dt>
<dd>Automated steps that build, test, and deploy software whenever code changes.</dd>

<dt>Pickle</dt>
<dd>A Python format for saving objects to a file; dangerous to load from untrusted sources
because it can execute code.</dd>

<dt>Software Composition Analysis (SCA)</dt>
<dd>Automatically inspecting a project's third-party dependencies for known
vulnerabilities.</dd>

<dt>AI firewall / guardrail</dt>
<dd>A layer that inspects and filters what goes into and comes out of an AI model to block
unsafe content.</dd>

</dl>
