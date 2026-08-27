from pathlib import Path

app_path=Path('src/app.js')
contract_path=Path('tests/ux_foundation_v2_contract.py')
app=app_path.read_text(encoding='utf-8')

replacements={
"}catch(err){showToast('Could not open the Trace project: '+String(err));}":"}catch(err){showActionError('Project could not be opened',err,'Trace could not open that project. Check that the project still exists and that Windows can access its folder, then try again.');}",
"catch(err){console.warn('Media preview unavailable',err);showToast('Media preview unavailable: '+String(err));}":"catch(err){console.warn('Media preview unavailable',err);showActionError('Media preview could not be opened',err,'Trace could not load this media preview. The source remains in your project. Check that the original media file is still available, then try again.');}",
"catch(err){showToast('Could not add coder: '+String(err));}":"catch(err){showActionError('Coder could not be added',err,'Trace could not add that coder. Existing coding and coder assignments are unchanged.');}",
"catch(err){showToast('Could not delete memo');}":"catch(err){showActionError('Memo could not be deleted',err,'Trace left the memo and its research links unchanged.');}",
"catch(err){showToast('Could not delete theme');}":"catch(err){showActionError('Theme could not be deleted',err,'Trace left the candidate theme, its code relationships and findings links unchanged.');}",
"catch(err){showToast('Could not delete selection: '+String(err));}":"catch(err){showActionError('Media selection could not be deleted',err,'Trace left the saved media selection and its coding unchanged.');}",
"catch(err){showToast('Could not rename collection');}":"catch(err){showActionError('Collection could not be renamed',err,'Trace left the collection name and its source membership unchanged.');}",
"catch(err){showToast('Could not delete collection');}":"catch(err){showActionError('Collection could not be deleted',err,'Trace left the collection and all source memberships unchanged.');}",
"if(!silent)showToast('Could not save findings: '+String(err));return null;":"if(!silent)showActionError('Findings could not be saved',err,'Trace could not save this findings draft. The text remains in the editor so you can copy it or try saving again.');return null;",
"catch(err){showToast('Could not link evidence: '+String(err));}":"catch(err){showActionError('Evidence could not be linked',err,'Trace could not attach that coded evidence to the findings section. The findings text and coding remain unchanged.');}",
"catch(err){showToast('Could not unlink evidence');}":"catch(err){showActionError('Evidence link could not be removed',err,'Trace left the evidence link attached to the findings section.');}",
"catch(err){showToast('Could not save annotation: '+String(err));}":"catch(err){showActionError('Annotation could not be saved',err,'Trace could not save that annotation. Existing annotations and coded passages are unchanged.');}",
"catch(err){showToast('Could not open project: '+String(err));}":"catch(err){showActionError('Portable project could not be opened',err,'Trace could not import that .trace project package. The current project is unchanged. Check the package and try again.');}",
"catch(err){showToast('Backup failed: '+String(err));}":"catch(err){showActionError('Backup could not be created',err,'Trace could not create a verified backup. Your working project is unchanged. Check available storage and project access, then try again.');}",
"catch(err){showToast('Portable export failed: '+String(err));}":"catch(err){showActionError('Portable project could not be exported',err,'Trace could not create the portable .trace package. Your project has not been changed. Check available storage and try again.');}",
"catch(err){showToast('Could not save media evidence: '+String(err));return;}":"catch(err){showActionError('Media evidence could not be saved',err,'Trace could not save that media selection and code relationship. Existing media and coding remain unchanged.');return;}",
"catch(err){showToast('Could not update source: '+String(err));return;}":"catch(err){showActionError('Source details could not be updated',err,'Trace could not save those source details. The source, participant relationship and collection memberships remain unchanged.');return;}",
"catch(err){showToast('Could not delete source');return;}":"catch(err){showActionError('Source could not be deleted',err,'Trace left the source and all attached coding, notes, evidence and relationships unchanged.');return;}",
"catch(err){showToast('Could not create collection');return;}":"catch(err){showActionError('Collection could not be created',err,'Trace could not create that collection. Your sources and existing collections are unchanged.');return;}",
"catch(err){showToast('Could not save backup policy');return;}":"catch(err){showActionError('Backup policy could not be saved',err,'Trace left the current automatic-backup settings unchanged.');return;}",
}

applied=[]
for old,new in replacements.items():
    if old in app:
        app=app.replace(old,new,1);applied.append(old)
    elif new not in app:
        raise SystemExit('Human-error anchor changed: '+old[:100])

# These research-write paths were already plain language but still provided no recovery context.
secondary={
"catch(err){console.error(err);showToast('Could not save coding mode to the local project');return;}":"catch(err){console.error(err);showActionError('Coding mode could not be changed',err,'Trace left the current coding mode unchanged. Close any other Trace window using this project and try again.');return;}",
"catch(err){console.error(err);showToast('Could not create the suggested code');return;}":"catch(err){console.error(err);showActionError('Suggested code could not be created',err,'Trace could not turn that suggestion into a project code. Existing codes and coding are unchanged.');return;}",
"catch(err){console.error(err);showToast('Could not record rejection');return;}":"catch(err){console.error(err);showActionError('Suggestion review could not be saved',err,'Trace could not record that rejection. No coding was applied.');return;}",
"catch(err){console.error(err);showToast('Could not save this coding reference');return;}":"catch(err){console.error(err);showActionError('Coding could not be saved',err,'Trace could not attach that code to the selected evidence. Existing coding remains unchanged.');return;}",
"catch(err){console.error(err);showToast('Could not create attribute');return;}":"catch(err){console.error(err);showActionError('Participant attribute could not be created',err,'Trace could not create that attribute. Existing participant data is unchanged.');return;}",
"catch(err){console.error(err);showToast('Could not save attribute value');return;}":"catch(err){console.error(err);showActionError('Participant attribute could not be saved',err,'Trace could not save that value. The participant record remains unchanged.');return;}",
"catch(err){console.error(err);btn.disabled=false;showToast('Could not create evidence link');}":"catch(err){console.error(err);btn.disabled=false;showActionError('Evidence link could not be created',err,'Trace could not create that evidence link. The source and current analysis remain unchanged.');}",
}
for old,new in secondary.items():
    if old in app:
        app=app.replace(old,new,1);applied.append(old)
    elif new not in app:
        raise SystemExit('Secondary human-error anchor changed: '+old[:100])

app_path.write_text(app,encoding='utf-8')
contract=contract_path.read_text(encoding='utf-8')
for assertion in (
    "assert 'Project could not be opened' in app\n",
    "assert 'Backup could not be created' in app\n",
    "assert 'Media evidence could not be saved' in app\n",
    "assert 'Participant attribute could not be saved' in app\n",
    "assert \"showToast('Could not open the Trace project: '+String(err))\" not in app\n",
    "assert \"showToast('Backup failed: '+String(err))\" not in app\n",
    "assert \"showToast('Portable export failed: '+String(err))\" not in app\n",
):
    if assertion not in contract:contract+='\n'+assertion
contract_path.write_text(contract,encoding='utf-8')

# Guard the important rule itself: user-facing catch paths should no longer concatenate raw exceptions
# for the research workflows completed here. Console logging remains allowed for troubleshooting.
check=app_path.read_text(encoding='utf-8')
for forbidden in (
    "Could not open the Trace project: '+String(err)",
    "Could not add coder: '+String(err)",
    "Could not delete selection: '+String(err)",
    "Could not save findings: '+String(err)",
    "Could not link evidence: '+String(err)",
    "Could not save annotation: '+String(err)",
    "Could not open project: '+String(err)",
    "Backup failed: '+String(err)",
    "Portable export failed: '+String(err)",
    "Could not save media evidence: '+String(err)",
    "Could not update source: '+String(err)",
):
    if forbidden in check:raise SystemExit('Raw user-facing error remains: '+forbidden)
print(f'Remaining human error states completed ({len(applied)} paths hardened)')
