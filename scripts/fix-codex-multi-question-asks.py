from pathlib import Path

path = Path("server/drivers/codex.ts")
text = path.read_text()
needle = '''        const requestId = newId();
        const summary =
'''
insert = '''        if (isQuestion && Array.isArray(params.questions) && params.questions.length > 1) {
          const questions = params.questions;
          const answers: Record<string, { answers: string[] }> = {};
          let questionIndex = 0;
          const openQuestion = () => {
            const question = questions[questionIndex];
            const requestId = newId();
            const summary = String(question.question ?? question.header ?? "Question");
            const choices = (question.options ?? []).map((option: any) => option.label).slice(0, 5);
            const finish = (behavior: "allow" | "deny" | "answer", message?: string, source: "user" | "timeout" | "system" = "user") => {
              if (!asks.delete(requestId)) return;
              clearTimeout(timer);
              answers[question.id] = { answers: [message || QUESTION_TIMEOUT_NOTE] };
              emit({ ...base(threadId, turnId), type: "request.resolved", requestId, behavior, source });
              questionIndex += 1;
              if (questionIndex < questions.length) openQuestion();
              else send({ jsonrpc: "2.0", id: msg.id, result: { answers } });
            };
            const timer = setTimeout(() => finish("answer", QUESTION_TIMEOUT_NOTE, "timeout"), 15 * 60_000);
            timer.unref?.();
            asks.set(requestId, finish);
            emit({
              ...base(threadId, turnId),
              type: "request.opened",
              requestId,
              requestType: "question",
              tool,
              summary,
              choices,
              approvalScope: controlsHost ? "local-computer" : undefined,
            });
          };
          openQuestion();
          return;
        }
        const requestId = newId();
        const summary =
'''
count = text.count(needle)
if count != 1:
    raise SystemExit(f"expected one request broker insertion point, found {count}")
path.write_text(text.replace(needle, insert, 1))
