<script>
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text/index";
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import CharacterCounter from "@smui/textfield/character-counter/index";
  import Button, { Label, Icon } from "@smui/button";
  import Paper from "@smui/paper";
  import IssueReportDialog from "./IssueReportDialog.svelte";

  let inputText = "";
  let romanizedText = "";
  let isRomanizing = false;
  let isFetchingRandomSentence = false;
  let showIssueReportDialog = false;

  const romanize = async () => {
    isRomanizing = true;
    const response = await fetch("api/romanize/?text=" + inputText);
    romanizedText = await response.text();
    isRomanizing = false;
  };

  const get_random_sentence = async () => {
    isFetchingRandomSentence = true;
    const response = await fetch("api/random_sentence");
    inputText = await response.text();
    isFetchingRandomSentence = false;
    romanize();
  };

  const openIssueReportDialog = async () => {
    await romanize();
    showIssueReportDialog = true;
  };
</script>

<LayoutGrid>
  <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 4 }}>
    <div class="input-container">
      <Paper elevation={0}>
        <Button
          disabled={isFetchingRandomSentence}
          color="secondary"
          on:click={get_random_sentence}
        >
          <Icon class="material-icons">shuffle</Icon>
          <Label>Try a random sentence</Label>
        </Button>
        <Textfield
          textarea
          style="width: 100%;"
          input$style="font-family: 'Noto Sans KR', sans-serif;"
          helperLine$style="width: 100%;"
          bind:value={inputText}
          label="Korean Text"
          input$maxlength="100"
        >
          <CharacterCounter slot="internalCounter">0 / 100</CharacterCounter>
          <HelperText slot="helper"
            >Enter a Korean word or phrase you want to romanize.</HelperText
          >
        </Textfield>
      </Paper>
    </div>
  </Cell>
  <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 4 }}>
    <div class="input-container">
      <Paper elevation={0}>
        <Button
          style="float: right;"
          color="secondary"
          on:click={openIssueReportDialog}
        >
          <Icon class="material-icons">flag</Icon>
          <Label>Report an issue</Label>
        </Button>
        <Textfield
          input$readonly="true"
          input$maxlength="10000"
          input$style="font-family: 'Noto Sans KR', sans-serif;"
          textarea
          style="width: 100%; background-color:whitesmoke; color:#FFF"
          bind:value={romanizedText}
          label="Romanized Result"
        >
          <CharacterCounter
            style="visibility: hidden;"
            slot="internalCounter"
          />
        </Textfield>
      </Paper>
    </div>
  </Cell>

  <Cell spanDevices={{ desktop: 3, tablet: 1, phone: 0 }} />
  <Cell spanDevices={{ desktop: 6, tablet: 6, phone: 4 }}>
    <div style="display:flex; justify-content: center; align-items: center;">
      <Button
        disabled={isRomanizing}
        variant="outlined"
        style="width:100%; font-family: 'Roboto', sans-serif; font-weight: 500;"
        on:click={romanize}
      >
        {#if isRomanizing === true}
          <Label>Romanizing...</Label>
        {:else}
          <Label>Romanize</Label>
        {/if}
      </Button>
    </div>
  </Cell>
  <Cell spanDevices={{ desktop: 3, tablet: 1, phone: 0 }} />
</LayoutGrid>
<IssueReportDialog
  bind:open={showIssueReportDialog}
  srcText={inputText}
  tgtText={romanizedText}
/>

<style>
  .input-container {
    height: 90%;
    padding: 4px 18px 18px;
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
</style>
