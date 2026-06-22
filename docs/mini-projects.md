# Mini-Projects Overview

Hands-On AI mini-projects are designed to provide hands-on learning experiences with large language models across different application types. These projects range from beginner to advanced levels and cover the various modules in Hands-On AI.

## Project Structure

Each mini-project follows a consistent structure:

- **Title and Difficulty Level**: Clearly indicates the project focus and complexity
- **Learning Objectives**: What students will accomplish and learn
- **Required Background**: Prerequisites and knowledge needed
- **Implementation Guide**: Step-by-step instructions
- **Extension Activities**: Ways to expand on the basic project
- **Assessment Criteria**: How to evaluate project success

## A note on type hints

The example code in these projects is written **without type hints** on purpose.
For someone still learning the language, annotations like
`def ask(self, prompt: str) -> str:` add reading overhead before the idea itself
has landed, so the examples stay deliberately plain to keep the focus on the
concept.

This is a teaching choice, not a recommendation against type hints:

- **For teachers:** the plain style is intentional. The `hands_on_ai` library
  *itself* is fully type-hinted and type-checked (`mypy`), so the package models
  good practice even though the project snippets keep things simple.
- **For advanced students:** adding type hints is a great extension exercise and
  reflects industry best practice. Annotate your project, run a type checker
  (`mypy` or `pyright`), and fix what it finds. Because the library ships type
  information, your editor and the checker will understand its functions too.

## Project Categories

### Chat Module Projects

Chat projects focus on creating conversational applications:

- **Personality Bots**: Custom chat personalities for specific purposes
- **Interactive Applications**: Goal-oriented conversation systems
- **Educational Assistants**: Subject-specific tutoring systems
- **Creative Writing**: Story generation and creative applications

### RAG Module Projects

Retrieval-Augmented Generation projects combine document processing with LLMs:

- **Custom Knowledge Bases**: Creating systems that answer questions from specific sources
- **Document Analysis**: Processing and extracting information from documents
- **Hybrid Systems**: Combining retrieval with additional processing

### Agent Module Projects

Agent projects implement tool-using, reasoning systems:

- **Custom Tool Creation**: Building specialized tools for agents
- **Multi-step Problem Solving**: Complex reasoning tasks
- **Domain-specific Assistants**: Specialized agents for particular fields

## How to Use These Projects

1. Browse the [Project Gallery](projects/index.md) to find a suitable project
2. Review the project documentation to understand requirements
3. Follow the implementation guide, making adaptations as needed
4. Use the provided starter code and templates when available
5. Evaluate based on the assessment criteria

## Project Implementation Workflow

1. **Setup**: Configure the required environment and dependencies
2. **Planning**: Sketch the solution approach and identify key components
3. **Implementation**: Code the solution, following the project guide
4. **Testing**: Verify functionality with appropriate test cases
5. **Extension**: Add additional features or improvements
6. **Documentation**: Add comments and documentation for your code

## Contributing New Projects

If you'd like to contribute a new mini-project:

1. Use the [Project Template](mini-project-template.md) as a starting point
2. Ensure your project includes clear learning objectives
3. Provide a step-by-step implementation guide
4. Include sample code and expected outputs
5. Add assessment criteria and extension activities

## Using Projects in the Classroom

For educators, these projects can be:

- **Individual assignments**: Students complete projects independently
- **Group projects**: Teams collaborate on more complex implementations
- **In-class demonstrations**: Showcase capabilities and concepts
- **Course capstones**: Combined with other modules for comprehensive projects

See the [Education Guide](education-guide.md) for more information on integrating these projects into your curriculum.
