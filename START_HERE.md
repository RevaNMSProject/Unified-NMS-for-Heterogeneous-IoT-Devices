# ⚡ SUPER QUICK START - With Virtual Environment

## First Time Setup (Do Once)

```powershell
# 1. Setup virtual environment
.\setup_venv.ps1

# Wait for it to complete (installs all dependencies)
```

---

## Every Time You Want to Run NMS

```powershell
# Just run this one command:
.\run_with_venv.ps1

# Dashboard opens automatically at: http://localhost:5000
```

---

## That's It! 🎉

### What Happens Behind the Scenes:
✅ Virtual environment activated (isolated dependencies)  
✅ RESTCONF simulator starts  
✅ MQTT simulator starts (if Mosquitto available)  
✅ Main NMS system starts  
✅ Dashboard opens in browser  

### What You'll See:
- 3-4 terminal windows open
- Each showing real-time data collection
- Dashboard in browser with live monitoring

---

## Stopping the System

Press `Ctrl+C` in each terminal window.

---

## Troubleshooting

### First time and getting errors?
```powershell
# Make sure you ran setup first:
.\setup_venv.ps1

# Then try running again:
.\run_with_venv.ps1
```

### Execution policy error?
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
.\setup_venv.ps1
```

### Still having issues?
See `VENV_GUIDE.md` for detailed instructions.

---

## Why Virtual Environment?

✅ **No dependency conflicts** with other Python projects  
✅ **Clean installation** - won't mess up your system  
✅ **Easy to reset** - just delete `venv/` folder and re-run setup  
✅ **No permission issues** - installs in project folder  

---

## Commands Summary

| Command | Purpose | When |
|---------|---------|------|
| `.\setup_venv.ps1` | Setup environment | First time only |
| `.\run_with_venv.ps1` | Run NMS | Every time you start |

---

**That's literally all you need!** 🚀

For more details, see:
- `VENV_GUIDE.md` - Detailed virtual environment guide
- `README.md` - Full project documentation
- `QUICKSTART.md` - Alternative startup methods
