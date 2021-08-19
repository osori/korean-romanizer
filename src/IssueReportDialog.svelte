<script>
  import Dialog, { Title, Content, Actions } from "@smui/dialog";
  import Button, { Label } from "@smui/button";
  import Paper from "@smui/paper";

  import "@typeform/embed/build/css/widget.css";

  export let open;
  export let srcText;
  export let tgtText;

  const submitReport = async () => {
    await fetch("api/bug_report", {
      method: "POST",
      body: JSON.stringify({
        srcText,
        tgtText,
      }),
    });

    open = false;
    alert("Your report was submitted. Thanks!");
  };
</script>

<Dialog
  bind:open
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
  <Title id="simple-title">Apologies for the bug!</Title>
  <Content id="simple-content">
    <p>You are trying to send a bug report on the following result.</p>
    <div class="text-item">
      <Paper>
        <h4>Korean Text</h4>
        <p>{srcText}</p>
      </Paper>
    </div>
    <Paper>
      <h4>Romanized Result</h4>
      <p>{tgtText}</p>
    </Paper>
  </Content>
  <Actions>
    <Button on:click={submitReport}>
      <Label>Submit</Label>
    </Button>
  </Actions>
</Dialog>

<style>
  .text-item {
    padding-bottom: 1em;
  }
</style>
