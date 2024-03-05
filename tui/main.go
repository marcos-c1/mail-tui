package main

import (
	"fmt"
	"os"
	tea "github.com/charmbracelet/bubbletea"
)

type model struct {
	emails []string
	cursor int
	selected map[int]struct{}
}

func initialModel() model {
	return model {
		emails: []string{"Email 1", "Email 2", "Email 3"},
		selected: make(map[int]struct{}),
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String(){
		case "ctrl+c", "q":
			return m, tea.Quit

		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}
		case "down", "j":
			if m.cursor < len(m.choices)-1 {
				m.cursor++
			}
		case "enter", " ":
			_, ok := m.selected[m.cursor]
			if ok {
				delete(m.selected, m.cursor)
			} else {
				m.selected[m.cursor] = struct{}{}
			}
		}
	}
	return m, nil
}

func (m model) View() string {
	// Header
	s := "Gmail messages\n\n"

	for i, email := range m.emails {
		cursor := " " // no cursor
		if m.cursor == i {
			cursor = ">" // cursor
		}

		checked := " "
		if _, ok := m.selected[i]; ok {
			checked = "x" // selected
		}

		s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, email)
	} 

}
