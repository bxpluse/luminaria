import React, {useEffect, useState} from 'react';
import '@draft-js-plugins/static-toolbar/lib/plugin.css';
import {EditorState, convertFromRaw, convertToRaw} from 'draft-js';
import Editor, {createEditorStateWithText} from '@draft-js-plugins/editor';
import createToolbarPlugin, {Separator,} from '@draft-js-plugins/static-toolbar';
import {
    BoldButton,
    ItalicButton,
    OrderedListButton,
    UnderlineButton,
    UnorderedListButton
} from '@draft-js-plugins/buttons';
import './Notes.css';
import Container from "react-bootstrap/Container";
import MyButton from "../../components/MyButton";
import Request from "../../Requests";

const toolbarPlugin = createToolbarPlugin();
const { Toolbar } = toolbarPlugin;
const plugins = [toolbarPlugin];

function Notes() {

    return (
        <Container>
            <CustomEditor />
        </Container>
    )
}

function CustomEditor() {

    useEffect(() => {
        Request.POST_JSON('/exec/notes/load', {}).then(data => {
            const contentState = convertFromRaw(JSON.parse(data['content']));
            setEditorState(EditorState.createWithContent(contentState));
        });
    }, []);

    const [editorState, setEditorState] = useState(createEditorStateWithText(""));

    function onChange(editorState){
        setEditorState(editorState);
    }

    const editor = React.useRef(null);

    function focusEditor() {
        editor.current.focus();
    }

    return (
        <div>
            <div className={"editor"}
                 onClick={focusEditor}>
                <div style={{ padding:"1em" }}>
                    <Toolbar>
                        {
                            (externalProps) => (
                                <div>
                                    <BoldButton {...externalProps} />
                                    <ItalicButton {...externalProps} />
                                    <UnderlineButton {...externalProps} />
                                    <Separator {...externalProps} />
                                    <UnorderedListButton {...externalProps} />
                                    <OrderedListButton {...externalProps} />
                                </div>
                            )
                        }
                    </Toolbar>
                    <br/>
                    <Editor
                        editorState={editorState}
                        onChange={onChange}
                        plugins={plugins}
                        ref={editor}
                    />
                </div>
            </div>
            <MyButton text={"Save"}
                      onClick={() => save(JSON.stringify(convertToRaw(editorState.getCurrentContent())))}
            />
        </div>
    );
}

async function save(content) {
    const body = {content: content};
    await Request.POST_JSON('/exec/notes/save', body);
}

export default Notes;